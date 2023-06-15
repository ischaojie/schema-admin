import re


def normaliza_schema_name(name: str) -> str:
    """
    >>> normaliza_schema_name("User")
    'user'
    >>> normaliza_schema_name("UserSchema")
    'user_schema'
    """
    return re.sub(r"([A-Z])", r"_\1", name).lower().lstrip("_")
