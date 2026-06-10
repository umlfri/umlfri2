from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .connectionvisualcomponent import ConnectionVisualComponent as ConnectionVisualComponent, ConnectionVisualObject as ConnectionVisualObject
from _typeshed import Incomplete
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import ArrowOrientation as ArrowOrientation
from umlfri2.types.geometry import Transformation as Transformation
from umlfri2.ufl.types.complex import UflColorType as UflColorType, UflProportionType as UflProportionType
from umlfri2.ufl.types.enum import UflDefinedEnumType as UflDefinedEnumType, UflTypedEnumType as UflTypedEnumType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType

class ArrowDefinition:
    def __init__(self, id, path, center, rotation) -> None: ...
    @property
    def id(self): ...
    @property
    def path(self): ...

class ConnectionArrowObject(ConnectionVisualObject):
    def __init__(self, position, style, orientation, color, fill) -> None: ...
    def assign_points(self, points) -> None: ...
    def draw(self, canvas) -> None: ...

class ConnectionArrowComponent(ConnectionVisualComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(self, position, style, orientation=None, color=None, fill=None) -> None: ...
    def compile(self, type_context) -> None: ...
