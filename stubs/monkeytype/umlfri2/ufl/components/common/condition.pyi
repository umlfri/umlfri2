from typing import (
    Any,
    Iterator,
    List,
)
from umlfri2.ufl.components.base.component import Component
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.table import TableRow
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class ConditionComponent:
    def __init__(
        self,
        children: List[Component],
        condition: DynamicValueProvider
    ) -> None: ...
    def _get_semantic_children(self) -> Iterator[TableRow]: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def filter_children(self, context: Context) -> Iterator[Any]: ...


class ThenComponent:
    def compile(self, type_context: TypeContext) -> None: ...
