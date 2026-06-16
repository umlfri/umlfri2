from .controlcomponent import ControlComponent as ControlComponent
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.ufl.types.basic import UflBoolType as UflBoolType, UflIntegerType as UflIntegerType
from umlfri2.ufl.types.generic import UflAnyType as UflAnyType
from umlfri2.ufl.types.structured import UflIterableType as UflIterableType, UflVariableWithMetadataType as UflVariableWithMetadataType
from typing import (
    Iterator,
    List,
    Tuple,
    Union,
)
from umlfri2.ufl.components.common.condition import ConditionComponent
from umlfri2.ufl.components.text.textdata import TextDataComponent
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.table import TableRow
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.objects.immutable.object import UflObject
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType

class ForEachItemMetadata:
    def __init__(self, value: UflObject, count: int, index: int) -> None: ...
    @property
    def value(self) -> UflObject: ...
    @property
    def index(self): ...
    @property
    def count(self) -> int: ...
    @property
    def is_first(self): ...
    @property
    def is_last(self) -> bool: ...
    @staticmethod
    def build_node_metadata_type(
        item_type: Union[UflVariableWithMetadataType, UflObjectType]
    ) -> UflVariableWithMetadataType: ...

class ForEachComponent(ControlComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[Union[ConditionComponent, TableRow]],
        src: DynamicValueProvider,
        item: str
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def filter_children(
        self,
        context: Context
    ) -> Iterator[Union[Tuple[Context, TableRow], Tuple[Context, TextDataComponent]]]: ...
