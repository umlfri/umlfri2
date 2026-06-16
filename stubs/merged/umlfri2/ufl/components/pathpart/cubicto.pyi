from .pathpartcomponent import PathPartComponent as PathPartComponent
from _typeshed import Incomplete
from umlfri2.types.geometry import Point as Point
from umlfri2.ufl.types.basic import UflDecimalType as UflDecimalType

class CubicTo(PathPartComponent):
    ATTRIBUTES: Incomplete
    def __init__(self, x1, y1, x2, y2, x, y) -> None: ...
    def compile(self, type_context) -> None: ...
    def add_to_path(self, context, builder) -> None: ...
