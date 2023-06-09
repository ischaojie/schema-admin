import os

import pickledb
from flask import Flask
from schema_admin import Admin, BaseSchema, Field

here = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

db = pickledb.load(os.path.join(here, "data/db.json"), True)

schema_admin = Admin(app, database=db)


class Book(BaseSchema):
    title: str
    author: str
    press: str
    price: float = Field(..., gt=0)


class BookCustom(Book):
    class Config:
        title = "book2"


schema_admin.add_schema(Book)
schema_admin.add_schema(BookCustom)
