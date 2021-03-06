from ..valueproviders import DefaultValueProvider
from umlfri2.types.geometry import PathBuilder
from umlfri2.types.geometry import Size
from umlfri2.types.geometry import Transformation
from umlfri2.ufl.types.complex import UflColorType
from umlfri2.ufl.types.structured import UflNullableType
from ..base.componenttype import ComponentType
from .graphicalcomponent import GraphicalComponent, GraphicalObject


class PathObject(GraphicalObject):
    def __init__(self, path, fill, border):
        self.__fill = fill
        self.__border = border
        
        self.__path = path
        self.__real_path = path
    
    def assign_bounds(self, bounds):
        transform = Transformation.make_translate(bounds.top_left) * Transformation.make_scale2(bounds.size)
        
        self.__real_path = self.__path.transform(transform)
    
    def draw(self, canvas, shadow):
        canvas.draw_path(self.__real_path, self.__border, self.__fill)


class PathComponent(GraphicalComponent):
    ATTRIBUTES = {
        'fill': UflNullableType(UflColorType()),
        'border': UflNullableType(UflColorType()),
    }
    CHILDREN_TYPE = ComponentType.path_part

    def __init__(self, children, fill=None, border=None):
        super().__init__(children)
        
        self.__fill = fill or DefaultValueProvider(None)
        self.__border = border or DefaultValueProvider(None)

    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            fill=self.__fill,
            border=self.__border,
        )
        
        self._compile_children(type_context)
    
    def create_graphical_object(self, context, ruler, size):
        builder = PathBuilder()
        
        for local, part in self._get_children(context):
            part.add_to_path(local, builder)
        
        path = builder.build().transform(Transformation.make_scale2(Size(1/size.width, 1/size.height)))
        
        fill = self.__fill(context)
        border = self.__border(context)
        
        return PathObject(path, fill, border)
