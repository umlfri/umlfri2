from umlfri2.types.geometry import Size
from umlfri2.ufl.types import UflDecimalType
from .visualcomponent import VisualComponent, VisualObject


class GraphicsObject(VisualObject):
    def __init__(self, children):
        self.__children = children
    
    def assign_bounds(self, bounds):
        for child in self.__children:
            child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return Size(0, 0)
    
    def draw(self, canvas, shadow):
        for child in self.__children:
            child.draw(canvas, shadow)
    
    def is_resizable(self):
        return False, False


class GraphicsComponent(VisualComponent):
    ATTRIBUTES = {
        'width': UflDecimalType(),
        'height': UflDecimalType(),
    }
    CHILDREN_TYPE = 'graphic'
    
    def __init__(self, children, width, height):
        super().__init__(children)
        self.__width = width
        self.__height = height
    
    def _create_object(self, context, ruler):
        width = self.__width(context)
        height = self.__height(context)
        
        size = Size(width, height)
        
        children = [
            child.create_graphical_object(local, ruler, size) for local, child in self._get_children(context)
        ]
        
        return GraphicsObject(children)
    
    def compile(self, variables):
        self._compile_expressions(
            variables,
            width=self.__width,
            height=self.__height,
        )
        
        self._compile_children(variables)
