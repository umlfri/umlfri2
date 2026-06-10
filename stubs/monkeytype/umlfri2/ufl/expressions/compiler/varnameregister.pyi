from typing import (
    Callable,
    Dict,
    Type,
    Union,
)
from umlfri2.types.enums.fontstyle import FontStyle


class VariableNameRegister:
    def __init__(self, user_variable_prefix: str) -> None: ...
    def build_globals(
        self
    ) -> Dict[str, Union[Type[bool], Type[str], Callable, Type[FontStyle]]]: ...
    def register_class(self, class_: Type[FontStyle]) -> str: ...
    def register_function(self, function: Union[Type[bool], Callable, Type[str]]) -> str: ...
    def register_temp_variable(self) -> str: ...
