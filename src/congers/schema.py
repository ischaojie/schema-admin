from __future__ import annotations

from pydantic import BaseModel, Field


class Model(BaseModel):
    schema_: dict = Field(alias="schema")
    data: dict


class ModelMetadata(BaseModel):
    name: str | None = None
    icon: str | None = None


class Metadata(BaseModel):
    title: str = "Conger"
    icon: str = ""
    total: int
    models: list[ModelMetadata] = []
