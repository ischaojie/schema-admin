from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
)

from pydantic.fields import Undefined, Field as _Field
from pydantic.typing import NoArgAnyCallable
from pydantic.color import Color as _Color
from pydantic.fields import ModelField

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny


def Field(
    default: Any = Undefined,
    *,
    default_factory: Optional[NoArgAnyCallable] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny", Any]] = None,
    include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny", Any]] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    allow_inf_nan: Optional[bool] = None,
    max_digits: Optional[int] = None,
    decimal_places: Optional[int] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique_items: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allow_mutation: bool = True,
    regex: Optional[str] = None,
    discriminator: Optional[str] = None,
    repr: bool = True,
    widget: Optional[str] = None,
    **extra: Any,
) -> Any:
    _extra = dict(
        widget=widget,
        **extra,
    )
    return _Field(
        default=default,
        default_factory=default_factory,
        alias=alias,
        title=title,
        description=description,
        exclude=exclude,
        include=include,
        const=const,
        gt=gt,
        ge=ge,
        lt=lt,
        le=le,
        multiple_of=multiple_of,
        allow_inf_nan=allow_inf_nan,
        max_digits=max_digits,
        decimal_places=decimal_places,
        min_items=min_items,
        max_items=max_items,
        unique_items=unique_items,
        min_length=min_length,
        max_length=max_length,
        allow_mutation=allow_mutation,
        regex=regex,
        discriminator=discriminator,
        repr=repr,
        **_extra,
    )


class Color(_Color):
    @classmethod
    def __modify_schema__(
        cls, field_schema: dict[str, Any], field: ModelField | None
    ) -> None:
        super().__modify_schema__(field_schema)
        if field and field.default:
            field_schema.update(default=field.default.as_hex())
