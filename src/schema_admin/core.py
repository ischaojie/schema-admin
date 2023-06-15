from __future__ import annotations

import json
from schema_admin.model import BaseSchema

from flask import (
    Blueprint,
    Flask,
    abort,
    jsonify,
    render_template,
    request,
)
from flask_cors import CORS

from schema_admin.database import Database
from schema_admin.schema import Metadata, Schema, SchemaMetadata
from schema_admin.utils import normaliza_schema_name


def load_package_files(path: str):
    import importlib.resources

    pkg, path = path.split("/", maxsplit=1)
    return importlib.resources.files(pkg).joinpath(path)


class BaseAdmin:
    def __init__(
        self,
        app: Flask,
        database: Database,
        title: str = "Admin",
        description: str | None = None,
    ) -> None:
        self.app = app
        self.database = database
        self.title = title
        self.description = description
        self.key_prefix = "schemas"

        self.admin = Blueprint(
            "admin",
            __name__,
            static_folder=load_package_files("schema_admin/static"),
            template_folder=load_package_files("schema_admin/templates"),
        )
        self.api = Blueprint("api", __name__)
        self._schemas: dict[str, type[BaseSchema]] = {}

    def add_schema(self, schema: type[BaseSchema]) -> None:
        name = schema.__config__.title if schema.__config__.title else schema.__name__
        self._schemas[name] = schema

    def metadata(self):
        model_metadata = []
        for name, schema in self._schemas.items():
            _metadata = SchemaMetadata(name=name, icon=schema.__config__.icon)
            model_metadata.append(_metadata)
        metadata = Metadata(
            title=self.title,
            total=len(model_metadata),
            schemas=model_metadata,
        )
        return metadata.dict()

    def get_schema_key(self, name: str) -> str:
        """
        key pattern will be: `key_prefix:key_name`
        """
        schema = self._schemas.get(name)
        if not schema:
            return f"{self.key_prefix}:{name}"

        schema_key_name = schema.__config__.key_name
        if schema_key_name:
            return f"{self.key_prefix}:{schema_key_name}"

        schema_name = normaliza_schema_name(schema.__name__)
        return f"{self.key_prefix}:{schema_name}"

    def get_schema_data(self, name: str) -> dict | None:
        schema = self._schemas.get(name)
        if not schema:
            return None
        key_prefix = self.get_schema_key(name)
        data = self.database.get(key_prefix)
        if not data:
            return None
        return json.loads(data)

    def save_model_data(self, name: str, value: dict) -> bool:
        schema = self._schemas.get(name)
        if not schema:
            return False
        key_prefix = self.get_schema_key(name)
        data = json.dumps(value)
        return bool(self.database.set(key_prefix, data))

    def register_error(self):
        self.app.register_error_handler(404, self.error_404)
        self.app.register_error_handler(400, self.error_400)

    def error_404(self, e):
        return jsonify(error=str(e)), 404

    def error_400(self, e):
        return jsonify(error=str(e)), 400


class Admin(BaseAdmin):
    """
    from flask import Flask
    from schema_admin import Admin, BaseSchema
    from pydantic import BaseSchema

    app = Flask(__name__)
    schema_admin = Admin(app)

    class Schema(BaseSchema):
        name: str
        desc: str = "this is description"
        age: int

    schema_admin.add_schema(User)
    """

    def __init__(
        self,
        app: Flask,
        database,
        url_prefix: str = "/admin",
        theme: str = "default",
        title: str = "Admin",
        description: str | None = None,
    ) -> None:
        self.url_prefix = url_prefix
        self.theme = theme

        super().__init__(
            app,
            database=database,
            title=title,
            description=description,
        )

        self.enable_cors()
        self._register_router()

    def enable_cors(self):
        CORS(self.app)

    def _register_router(self):
        self._register_api_router()
        self.admin.add_url_rule("/", view_func=self.index, methods=["GET"])
        self.admin.add_url_rule("/<path:path>", view_func=self.index, methods=["GET"])
        self.admin.register_blueprint(self.api, url_prefix="/api")
        self.app.register_blueprint(self.admin, url_prefix=self.url_prefix)

    def _register_api_router(self):
        self.api.add_url_rule("/", view_func=self.api_index, methods=["GET"])
        self.api.add_url_rule("/schemas", view_func=self.get_schemas, methods=["GET"])
        self.api.add_url_rule(
            "/schemas/<name>", view_func=self.get_schema, methods=["GET"]
        )
        self.api.add_url_rule(
            "/schemas/<name>/data", view_func=self.post_schema_data, methods=["POST"]
        )

    def index(self, path=""):
        manifest_file = load_package_files("schema_admin/static/manifest.json")
        with open(manifest_file, "r") as f:
            manifest = f.read()

        manifest = json.loads(manifest)
        context = {
            "title": self.title,
            "description": self.description,
            "manifest": manifest,
        }
        return render_template("index.html", **context)

    def api_index(self):
        return self.metadata()

    def get_schemas(self):
        model_list = [{name: schema.schema()} for name, schema in self._schemas.items()]
        return {"models": model_list, "total": len(self._schemas)}

    def get_schema(self, name: str) -> dict:
        schema = self._schemas.get(name)
        schema = schema and schema.schema() or {}
        model_data = self.get_schema_data(name)
        return Schema(struct=schema, data=model_data or {}).dict(by_alias=True)

    def post_schema_data(self, name: str) -> dict:
        schema = self._schemas.get(name)
        if not schema:
            abort(404, "Schema data not found")

        data = request.get_json()
        saved = self.save_model_data(name, data)
        return {"msg": saved}
