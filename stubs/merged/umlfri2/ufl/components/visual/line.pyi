from ..valueproviders import DefaultValueProvider as DefaultValueProvider
from .hbox import HBoxComponent as HBoxComponent
from .table import TableColumn as TableColumn, TableRow as TableRow
from .vbox import VBoxComponent as VBoxComponent
from .visualcomponent import VisualComponent as VisualComponent, VisualObject as VisualObject
from _typeshed import Incomplete
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import LineOrientation as LineOrientation
from umlfri2.types.geometry import Size as Size
from umlfri2.types.threestate import Maybe as Maybe
from umlfri2.ufl.types.complex import UflColorType as UflColorType
from umlfri2.ufl.types.enum import UflTypedEnumType as UflTypedEnumType

class LineObject(VisualObject):
    def __init__(self, orientation, color) -> None: ...
    def assign_bounds(self, bounds) -> None: ...
    def get_minimal_size(self): ...
    def draw(self, canvas, shadow) -> None: ...
    def is_resizable(self): ...

class LineComponent(VisualComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(self, orientation=None, color=None) -> None: ...
    def compile(self, type_context) -> None: ...
