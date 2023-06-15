from __future__ import annotations

from pydantic import BaseModel


class Schema(BaseModel):
    struct: dict
    data: dict


class SchemaMetadata(BaseModel):
    name: str | None = None
    icon: str | None = None


class Metadata(BaseModel):
    title: str = "Admin"
    total: int
    schemas: list[SchemaMetadata] = []
