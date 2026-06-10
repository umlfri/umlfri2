from typing import (
    Dict,
    Union,
)
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectType


def check_any(
    type: Union[UflStringType, UflObjectType],
    data: Union[str, Dict[str, str]]
) -> Union[str, Dict[str, str]]: ...


def check_object(type: UflObjectType, data: Dict[str, str]) -> Dict[str, str]: ...
