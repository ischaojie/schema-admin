from __future__ import annotations

from pydantic import BaseModel


class Schema(BaseModel):
    # The struct of this schema
    struct: dict
    # Options for UI
    ui: dict
    # THe form data
    data: dict


class SchemaMetadata(BaseModel):
    name: str | None = None
    id: str | None = None
    icon: str | None = None


class Metadata(BaseModel):
    title: str = "Admin"
    total: int
    schemas: list[SchemaMetadata] = []
