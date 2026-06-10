from umlfri2.types.geometry.path import PathBuilder
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext


class MoveTo:
    def __init__(
        self,
        x: ConstantValueProvider,
        y: ConstantValueProvider
    ) -> None: ...
    def add_to_path(
        self,
        context: Context,
        builder: PathBuilder
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
