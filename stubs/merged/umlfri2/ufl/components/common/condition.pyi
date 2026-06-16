from ..base.helpercomponent import HelperComponent as HelperComponent
from .controlcomponent import ControlComponent as ControlComponent
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.ufl.types.basic import UflBoolType as UflBoolType
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

class ThenComponent(HelperComponent):
    def compile(self, type_context: TypeContext) -> None: ...

class ElseComponent(HelperComponent):
    def compile(self, type_context) -> None: ...

class ConditionComponent(ControlComponent):
    ATTRIBUTES: Incomplete
    SPECIAL_CHILDREN: Incomplete
    def __init__(
        self,
        children: List[Component],
        condition: DynamicValueProvider
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def filter_children(self, context: Context) -> Iterator[Any]: ...
