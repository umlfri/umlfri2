from typing import (
    Any,
    Optional,
)


class UflTypedEnumType:
    def __init__(self, type: Any, default: None = ...) -> None: ...
    def is_assignable_from(self, other: UflTypedEnumType) -> bool: ...
