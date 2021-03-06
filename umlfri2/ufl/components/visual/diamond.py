from umlfri2.types.geometry import Size, PathBuilder, Transformation
from umlfri2.types.threestate import Maybe
from umlfri2.ufl.types.complex import UflColorType
from ..valueproviders import DefaultValueProvider
from .visualcomponent import VisualObject, VisualComponent


class DiamondObject(VisualObject):
    def __init__(self, child, fill, border):
        self.__child = child
        self.__fill = fill
        self.__border = border
        self.__path = None
        
        if child is None:
            self.__child_size = Size(0, 0)
        else:
            self.__child_size = child.get_minimal_size()
    
    def assign_bounds(self, bounds):
        path = PathBuilder()
        path.move_to(bounds.left_center)
        path.line_to(bounds.top_center)
        path.line_to(bounds.right_center)
        path.line_to(bounds.bottom_center)
        path.close()
        
        self.__path = path.build()
        
        if self.__child is not None:
            self.__child.assign_bounds(bounds)
    
    def get_minimal_size(self):
        return self.__child_size
    
    def draw(self, canvas, shadow):
        if shadow:
            canvas.draw_path(
                self.__path.transform(Transformation.make_translate(shadow.shift)),
                None,
                shadow.color
            )
        else:
            canvas.draw_path(self.__path, self.__border, self.__fill)
            if self.__child is not None:
                self.__child.draw(canvas, None)
    
    def is_resizable(self):
        if self.__child is None:
            return False, False
        else:
            res_x, res_y = self.__child.is_resizable()
            
            if res_x is Maybe:
                res_x = True
            if res_y is Maybe:
                res_y = True
            
            return res_x, res_y


class DiamondComponent(VisualComponent):
    ATTRIBUTES = {
        'fill': UflColorType(),
        'border': UflColorType()
    }
    
    def __init__(self, children, fill=None, border=None):
        super().__init__(children)
        self.__fill = fill or DefaultValueProvider(None)
        self.__border = border or DefaultValueProvider(None)
    
    def _create_object(self, context, ruler):
        found_child = None
        for local, child in self._get_children(context):
            found_child = child._create_object(local, ruler)
            break
        
        return DiamondObject(found_child, self.__fill(context), self.__border(context))
    
    def compile(self, type_context):
        self._compile_expressions(
            type_context,
            fill=self.__fill,
            border=self.__border,
        )
        
        self._compile_children(type_context)
