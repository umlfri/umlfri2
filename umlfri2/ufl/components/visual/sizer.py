from umlfri2.types.threestate import Maybe
from ..expressions import NoneConstantExpression
from umlfri2.types.geometry import Size
from umlfri2.ufl.types import UflIntegerType, UflNullableType
from .visualcomponent import VisualComponent, VisualObject


class SizerObject(VisualObject):
    def __init__(self, child, minwidth, maxwidth, minheight, maxheight, width, height):
        self.__child = child
        self.__minwidth = minwidth
        self.__maxwidth = maxwidth
        self.__minheight = minheight
        self.__maxheight = maxheight
        self.__width = width
        self.__height = height
        
        if child is None:
            self.__child_size = Size(0, 0)
        else:
            self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        if self.__child is not None:
            self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        w = self.__child_size.width
        h = self.__child_size.height
        
        if self.__width is not None:
            w = self.__width
        else:
            if self.__minwidth is not None and w < self.__minwidth:
                w = self.__minwidth
            if self.__maxwidth is not None and w > self.__maxwidth:
                w = self.__maxwidth
        
        if self.__height is not None:
            h = self.__height
        else:
            if self.__minheight is not None and h < self.__minheight:
                h = self.__minheight
            if self.__maxheight is not None and w > self.__maxheight:
                h = self.__maxheight
        
        return Size(w, h)
            
    def draw(self, canvas, shadow):
        if self.__child is not None:
            self.__child.draw(canvas, shadow)
    
    def is_resizable(self):
        if self.__child is None:
            resizable_x = Maybe
            resizable_y = Maybe
        else:
            resizable_x, resizable_y = self.__child.is_resizable()
        
        if self.__width is not None:
            resizable_x = False
        
        if self.__height is not None:
            resizable_y = False
        
        return resizable_x, resizable_y


class SizerComponent(VisualComponent):
    ATTRIBUTES = {
        'minwidth': UflNullableType(UflIntegerType()),
        'maxwidth': UflNullableType(UflIntegerType()),
        'minheight': UflNullableType(UflIntegerType()),
        'maxheight': UflNullableType(UflIntegerType()),
        'width': UflNullableType(UflIntegerType()),
        'height': UflNullableType(UflIntegerType()),
    }
    
    def __init__(self, children, minwidth=None, maxwidth=None, minheight=None, maxheight=None, width=None, height=None):
        super().__init__(children)
        if (minwidth is not None or maxwidth is not None) and width is not None:
            raise Exception("You cannot specify min/max width together with absolute width")
        if (minheight is not None or maxheight is not None) and height is not None:
            raise Exception("You cannot specify min/max height together with absolute height")
        
        self.__minwidth = minwidth or NoneConstantExpression()
        self.__maxwidth = maxwidth or NoneConstantExpression()
        
        self.__minheight = minheight or NoneConstantExpression()
        self.__maxheight = maxheight or NoneConstantExpression()
        
        self.__width = width or NoneConstantExpression()
        self.__height = height or NoneConstantExpression()
    
    def _create_object(self, context, ruler):
        child_object = None
        for local, child in self._get_children(context):
            child_object = child._create_object(local, ruler)
            break
        
        return SizerObject(
            child_object,
            self.__minwidth(context),
            self.__maxwidth(context),
            self.__minheight(context),
            self.__maxheight(context),
            self.__width(context),
            self.__height(context)
        )
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            minwidth=self.__minwidth,
            maxwidth=self.__maxwidth,
            minheight=self.__minheight,
            maxheight=self.__maxheight,
            width=self.__width,
            height=self.__height,
        )
        
        self._compile_children(type_context)
