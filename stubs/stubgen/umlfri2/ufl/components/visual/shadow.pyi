from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from typing import NamedTuple
from umlfri2.types.color import Colors as Colors
from umlfri2.types.geometry import Vector as Vector
from umlfri2.ufl.types.basic import UflIntegerType as UflIntegerType
from umlfri2.ufl.types.complex import UflColorType as UflColorType

class ShadowInfo(NamedTuple):
    color: Incomplete
    shift: Incomplete

class ShadowObject(VisualObject):
    def __init__(self, child, color, padding) -> None: ...
    def assign_bounds(self, bounds) -> None: ...
    def get_minimal_size(self): ...
    def draw(self, canvas, shadow) -> None: ...
    def is_resizable(self): ...

class ShadowComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    def __init__(self, children, color=None, padding=None) -> None: ...
    def compile(self, type_context) -> None: ...
