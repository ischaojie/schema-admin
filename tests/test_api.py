from flask.testing import FlaskClient
from schema_admin.schema import SchemaMetadata, Schema
from .app import Book


def test_get_metadata(client: FlaskClient):
    rsp = client.get("/admin/api/")
    assert rsp.status_code == 200
    assert SchemaMetadata.parse_obj(rsp.json)


def test_get_schema(client: FlaskClient):
    rsp = client.get("/admin/api/schemas/book")
    assert rsp.status_code == 200
    assert Schema.parse_obj(rsp.json)


def test_get_schema_custom_title(client: FlaskClient):
    rsp = client.get("/admin/api/schemas/book2")
    assert rsp.status_code == 200
    assert Schema.parse_obj(rsp.json)


def test_post_schema_data(client: FlaskClient):
    book = Book(title="test", author="chaojie", press="test-press", price=20.1)
    rsp = client.post("/admin/api/schemas/book/data", json=book.dict())
    assert rsp.status_code == 200
