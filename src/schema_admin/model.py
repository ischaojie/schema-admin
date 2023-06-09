from __future__ import annotations

from pydantic import BaseConfig, BaseModel, Field


class SchemaConfig(BaseConfig):
    # The title for each schema
    title: str | None = None

    # The icon for each model
    icon: str | None = None

    # the prefix for key to saved into database
    key_prefix: str | None = None


class BaseSchema(BaseModel):
    Config = SchemaConfig
