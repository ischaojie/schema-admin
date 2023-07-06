from __future__ import annotations
from typing import Any
from pydantic import BaseConfig, BaseModel  # noqa


class SchemaConfig(BaseConfig):
    # The title will show in the admin, default to class name
    title: str | None = None

    # The icon for each model
    icon: str | None = None

    # the name for key to saved into database
    key_name: str | None = None


class BaseSchema(BaseModel):
    @classmethod
    def ui_schema(cls):
        schema = {}
        for name, field in cls.__fields__.items():
            widget = field.field_info.extra.get("widget")
            if not widget:
                continue
            schema[name] = {
                "ui:widget": widget,
            }
        return schema

    class Config(SchemaConfig):
        @staticmethod
        def schema_extra(schema: dict[str, Any], model: type["BaseSchema"]) -> None:
            for prop in schema.get("properties", {}).values():
                prop.pop("widget", None)
