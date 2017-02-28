from umlfri2.types.geometry import Point
from umlfri2.ufl.types import UflDecimalType
from .pathpartcomponent import PathPartComponent


class LineTo(PathPartComponent):
    ATTRIBUTES = {
        'x': UflDecimalType(),
        'y': UflDecimalType(),
    }

    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y

    def compile(self, variables):
        self._compile_expressions(
            variables,
            x=self.__x,
            y=self.__y,
        )

    def add_to_path(self, context, builder):
        x = self.__x(context)
        y = self.__y(context)

        builder.line_to(Point(x, y))
