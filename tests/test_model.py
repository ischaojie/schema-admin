from schema_admin import BaseSchema, Field


class BookSchema(BaseSchema):
    title: str = Field(..., title="Book Title", widget="text")


def test_ui_schema():
    ui_schema = BookSchema.ui_schema()
    print(ui_schema)
    assert ui_schema == {
        "title": {
            "ui:widget": "text",
        }
    }
