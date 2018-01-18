from umlfri2.types.enums import HorizontalAlignment, VerticalAlignment
from umlfri2.types.threestate import Maybe
from umlfri2.types.geometry import Rectangle
from umlfri2.ufl.types import UflTypedEnumType, UflNullableType
from .visualcomponent import VisualComponent, VisualObject
from ..expressions import ConstantExpression


class AlignObject(VisualObject):
    def __init__(self, child, horizontal, vertical):
        self.__child = child
        self.__horizontal = horizontal
        self.__vertical = vertical
        self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        x = bounds.x1
        y = bounds.y1
        w = bounds.width
        h = bounds.height
        
        w_inner = self.__child_size.width
        h_inner = self.__child_size.height
        
        if self.__horizontal == HorizontalAlignment.center:
            x += (w - w_inner) // 2
            w = w_inner
        elif self.__horizontal == HorizontalAlignment.left:
            w = w_inner
        elif self.__horizontal == HorizontalAlignment.right:
            x += w - w_inner
            w = w_inner
        
        if self.__vertical == VerticalAlignment.center:
            y += (h - h_inner) // 2
            h = h_inner
        elif self.__vertical == VerticalAlignment.top:
            h = h_inner
        elif self.__vertical == VerticalAlignment.bottom:
            y += h - h_inner
            h = h_inner
        
        self.__child.assign_bounds(Rectangle(x, y, w, h))
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        self.__child.draw(canvas, shadow)
    
    def is_resizable(self):
        resizable_x, resizable_y = self.__child.is_resizable()
        
        if self.__horizontal is not None:
            resizable_x = Maybe
        if self.__vertical is not None:
            resizable_y = Maybe
        
        return resizable_x, resizable_y


class AlignComponent(VisualComponent):
    ATTRIBUTES = {
        'horizontal': UflNullableType(UflTypedEnumType(HorizontalAlignment)),
        'vertical': UflNullableType(UflTypedEnumType(VerticalAlignment)),
    }
    
    def __init__(self, children, horizontal=None, vertical=None):
        super().__init__(children)
        self.__horizontal = horizontal or ConstantExpression(None)
        self.__vertical = vertical or ConstantExpression(None)
    
    def _create_object(self, context, ruler):
        for local, child in self._get_children(context):
            return AlignObject(
                child._create_object(local, ruler),
                self.__horizontal(context),
                self.__vertical(context)
            )
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            vertical=self.__vertical,
            horizontal=self.__horizontal,
        )
        
        self._compile_children(type_context)
