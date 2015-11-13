from umlfri2.types.geometry import Size
from .visualcomponent import VisualComponent, VisualObject


class EmptyObject(VisualObject):
    def assign_bounds(self, bounds):
        pass
    
    def get_minimal_size(self):
        return Size(0, 0)
            
    def draw(self, canvas, shadow):
        pass
    
    def is_resizable(self):
        return True, True


class EmptyComponent(VisualComponent):
    HAS_CHILDREN = False
    
    def __init__(self):
        super().__init__(())
    
    def _create_object(self, context, ruler):
        return EmptyObject()
