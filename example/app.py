from __future__ import annotations

from datetime import datetime
from enum import Enum

import pickledb
from schema_admin import BaseSchema, Admin, Field
from flask import Flask, redirect

app = Flask(__name__)

db = pickledb.load("./db.json", True)

schema_admin = Admin(
    app,
    database=db,
    title="My Admin",
    description="THis is my schema admin",
)


class FruitEnum(str, Enum):
    pear = "pear"
    banana = "banana"


class User(BaseSchema):
    """
    This is user schema description
    """
    name: str
    desc: str = "this is description"
    age: int = Field(..., gt=18, lt=100)
    student: bool
    fruit: FruitEnum = FruitEnum.pear
    created_at: datetime = datetime.now()

    class Config:
        icon = "fa-user"
        key_prefix = "user"


class Book(BaseSchema):
    title: str
    price: int

    class Config:
        icon = "fa-book"


schema_admin.add_schema(User)
schema_admin.add_schema(Book)


@app.get("/")
def index():
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
