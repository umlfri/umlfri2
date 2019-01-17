from umlfri2.types.geometry import Point
from umlfri2.ufl.types.basic import UflDecimalType
from .pathpartcomponent import PathPartComponent


class MoveTo(PathPartComponent):
    ATTRIBUTES = {
        'x': UflDecimalType(),
        'y': UflDecimalType(),
    }

    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y

    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            x=self.__x,
            y=self.__y,
        )

    def add_to_path(self, context, builder):
        x = self.__x(context)
        y = self.__y(context)
        
        builder.move_to(Point(x, y))
