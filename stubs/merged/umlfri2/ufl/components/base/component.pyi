from _typeshed import Incomplete
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
    ATTRIBUTES: Incomplete
    CHILDREN_ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    CHILDREN_TYPE: Incomplete
    IS_CONTROL: bool
    IS_HELPER: bool
    SPECIAL_CHILDREN: Incomplete
    ONLY_SPECIAL_CHILDREN: bool
    def __init__(self, children: Any) -> None: ...
    def compile(self, type_context) -> None: ...
