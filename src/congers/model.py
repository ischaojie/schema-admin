from __future__ import annotations

from pydantic import BaseConfig, BaseModel as _BaseModel, Field


class ModelConfig(BaseConfig):
    # The icon for each model
    icon: str | None = None

    # the prefix for key to saved into database
    key_prefix: str | None = None


class BaseModel(_BaseModel):
    Config = ModelConfig
