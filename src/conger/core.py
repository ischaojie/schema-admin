from __future__ import annotations

import json
from conger.model import BaseModel

from flask import (
    Blueprint,
    Flask,
    abort,
    jsonify,
    render_template,
    request,
)
from flask_cors import CORS

from conger.database import Database
from conger.schema import Metadata, Model, ModelMetadata


def load_package_files(path: str):
    import importlib.resources

    pkg, path = path.split("/", maxsplit=1)
    return importlib.resources.files(pkg).joinpath(path)


class BaseConger:
    def __init__(self, app: Flask, database: Database, title: str = "Conger") -> None:
        self.app = app
        self.database = database
        self.title = title
        self.key_prefix = "conger"

        self.admin = Blueprint(
            "conger",
            __name__,
            static_folder=load_package_files("conger/static"),
            template_folder=load_package_files("conger/templates"),
        )
        self.api = Blueprint("api", __name__)
        self._model: dict[str, type[BaseModel]] = {}

    def add_model(self, model: type[BaseModel]) -> None:
        self._model[model.__name__.lower()] = model

    def metadata(self):
        model_metadata = []
        for name, model in self._model.items():
            _metadata = ModelMetadata(name=name, icon=model.__config__.icon)
            model_metadata.append(_metadata)
        metadata = Metadata(
            title=self.title, models=model_metadata, total=len(model_metadata)
        )
        return metadata.dict()

    def get_model_key(self, name: str) -> str:
        model = self._model.get(name)
        if not model:
            return f"{self.key_prefix}:{name}"

        model_key_prefix = model.__config__.key_prefix
        return (
            model_key_prefix
            and f"{self.key_prefix}:{model_key_prefix}:{name}"
            or f"{self.key_prefix}:{name}"
        )

    def get_model_data(self, name: str) -> dict | None:
        model = self._model.get(name)
        if not model:
            return None
        key_prefix = self.get_model_key(name)
        data = self.database.get(key_prefix)
        if not data:
            return None
        return json.loads(data)

    def save_model_data(self, name: str, value: dict) -> bool:
        model = self._model.get(name)
        if not model:
            return False
        key_prefix = self.get_model_key(name)
        data = json.dumps(value)
        return bool(self.database.set(key_prefix, data))

    def register_error(self):
        self.app.register_error_handler(404, self.error_404)
        self.app.register_error_handler(400, self.error_400)

    def error_404(self, e):
        return jsonify(error=str(e)), 404

    def error_400(self, e):
        return jsonify(error=str(e)), 400


class Conger(BaseConger):
    """
    from flask import Flask
    from conger import Conger, BaseModel
    from pydantic import BaseModel

    app = Flask(__name__)
    conger = Conger(app)

    class User(BaseModel):
        name: str
        desc: str = "this is description"
        age: int

    conger.add_model(User)
    """

    def __init__(
        self,
        app: Flask,
        database,
        title: str = "Conger",
        url_prefix: str = "/conger",
        theme: str = "default",
    ) -> None:
        self.url_prefix = url_prefix
        self.theme = theme

        super().__init__(app, database=database, title=title)

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
        self.api.add_url_rule("/models", view_func=self.get_models, methods=["GET"])
        self.api.add_url_rule(
            "/models/<name>", view_func=self.get_model, methods=["GET"]
        )
        self.api.add_url_rule(
            "/models/<name>/data", view_func=self.post_model_data, methods=["POST"]
        )

    def index(self, path=""):
        manifest_file = load_package_files("conger/static/manifest.json")
        with open(manifest_file, "r") as f:
            manifest = f.read()

        manifest = json.loads(manifest)
        context = {
            "title": self.title,
            "manifest": manifest,
        }
        return render_template("index.html", **context)

    def api_index(self):
        return self.metadata()

    def get_models(self):
        model_list = [{name: model.schema()} for name, model in self._model.items()]
        return {"models": model_list, "total": len(self._model)}

    def get_model(self, name: str) -> dict:
        model = self._model.get(name)
        schema = model and model.schema() or {}
        model_data = self.get_model_data(name)
        print(Model(schema=schema, data=model_data or {}).dict(by_alias=True))
        return Model(schema=schema, data=model_data or {}).dict(by_alias=True)

    def post_model_data(self, name: str) -> dict:
        model = self._model.get(name)
        if not model:
            abort(404, "Model data not found")

        data = request.get_json()
        saved = self.save_model_data(name, data)
        return {"msg": saved}
