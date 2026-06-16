from .pathpartcomponent import PathPartComponent as PathPartComponent
from _typeshed import Incomplete
from umlfri2.types.geometry import Point as Point
from umlfri2.ufl.types.basic import UflDecimalType as UflDecimalType
from umlfri2.types.geometry.path import PathBuilder
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class MoveTo(PathPartComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        x: ConstantValueProvider,
        y: ConstantValueProvider
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def add_to_path(
        self,
        context: Context,
        builder: PathBuilder
    ) -> None: ...
