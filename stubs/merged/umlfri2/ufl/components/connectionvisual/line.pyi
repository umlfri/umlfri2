from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .connectionvisualcomponent import ConnectionVisualComponent as ConnectionVisualComponent, ConnectionVisualObject as ConnectionVisualObject
from _typeshed import Incomplete
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import LineStyle as LineStyle
from umlfri2.types.geometry import PathBuilder as PathBuilder
from umlfri2.types.proportion import EMPTY_PROPORTION as EMPTY_PROPORTION, WHOLE_PROPORTION as WHOLE_PROPORTION
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflProportionType as UflProportionType
from umlfri2.ufl.types.enum import UflTypedEnumType as UflTypedEnumType

class ConnectionLineObject(ConnectionVisualObject):
    def __init__(self, start, end, style, color) -> None: ...
    def assign_points(self, points) -> None: ...
    def draw(self, canvas) -> None: ...

class ConnectionLineComponent(ConnectionVisualComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(self, start=None, end=None, style=None, color=None) -> None: ...
    def compile(self, type_context) -> None: ...
