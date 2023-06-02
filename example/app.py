from datetime import datetime
from enum import Enum

import pickledb
from conger import BaseModel, Conger, Field
from flask import Flask, redirect

app = Flask(__name__)

db = pickledb.load("db.json", True)

conger = Conger(app, database=db)


class FruitEnum(str, Enum):
    pear = "pear"
    banana = "banana"


class User(BaseModel):
    name: str
    desc: str = "this is description"
    age: int = Field(..., gt=18, lt=100)
    student: bool
    fruit: FruitEnum = FruitEnum.pear
    created_at: datetime = datetime.now()

    class Config:
        icon = "fa-user"
        key_prefix = "user"


class Book(BaseModel):
    title: str
    price: int

    class Config:
        icon = "fa-book"


conger.add_model(User)
conger.add_model(Book)


@app.get("/")
def index():
    return redirect("/conger")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
