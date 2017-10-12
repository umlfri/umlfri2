from umlfri2.types.geometry import Point
from umlfri2.ufl.types import UflDecimalType
from .pathpartcomponent import PathPartComponent


class CubicTo(PathPartComponent):
    ATTRIBUTES = {
        'x1': UflDecimalType(),
        'y1': UflDecimalType(),
        'x2': UflDecimalType(),
        'y2': UflDecimalType(),
        'x': UflDecimalType(),
        'y': UflDecimalType(),
    }

    def __init__(self, x1, y1, x2, y2, x, y):
        super().__init__()
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__x = x
        self.__y = y

    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            x1=self.__x1,
            y1=self.__y1,
            x2=self.__x2,
            y2=self.__y2,
            x=self.__x,
            y=self.__y,
        )

    def add_to_path(self, context, builder):
        x1 = self.__x1(context)
        y1 = self.__y1(context)
        x2 = self.__x2(context)
        y2 = self.__y2(context)
        x = self.__x(context)
        y = self.__y(context)

        builder.cubic_to(Point(x1, y1), Point(x2, y2), Point(x, y))
