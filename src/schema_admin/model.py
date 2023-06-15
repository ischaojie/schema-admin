from __future__ import annotations

from pydantic import BaseConfig, BaseModel, Field  # noqa


class SchemaConfig(BaseConfig):
    # The title will show in the admin, default to class name
    title: str | None = None

    # The icon for each model
    icon: str | None = None

    # the name for key to saved into database
    key_name: str | None = None


class BaseSchema(BaseModel):
    Config = SchemaConfig
