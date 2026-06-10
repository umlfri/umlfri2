from typing import (
    Any,
    Iterator,
    Optional,
    Union,
)
from umlfri2.ufl.components.common.foreach import ForEachItemMetadata
from umlfri2.ufl.objects.immutable.object import UflObject


class Context:
    def __init__(self) -> None: ...
    def get_variables(self, names: Iterator[Any]) -> Iterator[Any]: ...
    def set_variable(
        self,
        name: str,
        item: Optional[Union[int, ForEachItemMetadata, UflObject, str]]
    ) -> Context: ...
