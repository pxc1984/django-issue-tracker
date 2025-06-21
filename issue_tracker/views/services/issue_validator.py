from enum import Enum
from typing import Any

def try_int(value: Any) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None

def validate_in_enum(value: Any, target_type) -> tuple[bool, int]:
    if not issubclass(target_type, Enum):
        raise TypeError

    if not value:
        return True, 0

    value_int = try_int(value)
    if value_int is not None:
        if value_int not in target_type:
            return False, 0
        return True, value_int
    elif isinstance(value, str):
        if value in target_type.__members__:
            return True, target_type[value].value
        return False, 0
    else:
        return False, 0
