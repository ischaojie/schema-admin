from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Database(Protocol):
    def get(self, key: str, ):
        ...

    def set(self, key: str, value):
        ...

    def delete(self, key: str) -> bool:
        ...
