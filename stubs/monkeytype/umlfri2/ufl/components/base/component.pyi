from typing import (
    Any,
    Iterator,
    Union,
)
from umlfri2.ufl.components.common.condition import (
    ConditionComponent,
    ThenComponent,
)
from umlfri2.ufl.components.visual.table import TableRow
from umlfri2.ufl.components.visual.vbox import VBoxComponent
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType


class Component:
    def __init__(self, children: Any) -> None: ...
    def _change_attribute_type(self, attrname: str, type: UflStringEnumType) -> None: ...
    def _compile_child_expressions(
        self,
        type_context: TypeContext,
        **expressions
    ) -> None: ...
    def _compile_children(self, type_context: TypeContext) -> None: ...
    def _compile_expressions(self, type_context: TypeContext, **expressions) -> None: ...
    def _get_children(self, context: Context) -> Iterator[Any]: ...
    def _get_parent(
        self
    ) -> Union[VBoxComponent, ThenComponent, ConditionComponent]: ...
    def _get_semantic_children(self) -> Iterator[TableRow]: ...
