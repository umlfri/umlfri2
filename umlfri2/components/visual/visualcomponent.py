from ..base.component import Component
from umlfri2.components.visual.visualobjectcontainer import VisualObjectContainer


class VisualObject:
    def assign_bounds(self, bounds):
        raise NotImplementedError
    
    def get_minimal_size(self):
        raise NotImplementedError
    
    def draw(self, canvas, shadow):
        raise NotImplementedError


class VisualComponent(Component):
    def is_control(self):
        return False
    
    def is_resizable(self, context):
        ret_x = False
        ret_y = False
        for child, local in self._get_children(context):
            child_x, child_y = child.is_resizable(local)
            
            ret_x = ret_x or child_x
            ret_y = ret_y or child_y
            
            if ret_x and ret_y:
                return ret_x, ret_y
        
        return ret_x, ret_y
    
    def _create_object(self, context, ruler):
        raise NotImplementedError
    
    def create_visual_object(self, context, ruler):
        return VisualObjectContainer(self._create_object(context, ruler))
