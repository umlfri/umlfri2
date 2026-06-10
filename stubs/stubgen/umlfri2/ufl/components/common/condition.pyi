from ..base.helpercomponent import HelperComponent as HelperComponent
from .controlcomponent import ControlComponent as ControlComponent
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.ufl.types.basic import UflBoolType as UflBoolType

class ThenComponent(HelperComponent):
    def compile(self, type_context) -> None: ...

class ElseComponent(HelperComponent):
    def compile(self, type_context) -> None: ...

class ConditionComponent(ControlComponent):
    ATTRIBUTES: Incomplete
    SPECIAL_CHILDREN: Incomplete
    def __init__(self, children, condition) -> None: ...
    def compile(self, type_context) -> None: ...
    def filter_children(self, context) -> Generator[Incomplete, Incomplete]: ...
