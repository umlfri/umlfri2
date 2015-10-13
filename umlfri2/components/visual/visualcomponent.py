from ..base.component import Component


class VisualObject:
    def assign_bounds(self, bounds):
        raise NotImplementedError
    
    def get_minimal_size(self):
        raise NotImplementedError
    
    def draw(self, canvas, shadow, shadow_shift):
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
    
    def get_minimal_size(self, context, ruler):
        obj = self._create_object(context, ruler)
        return obj.get_minimal_size()
    
    def _create_object(self, context, ruler):
        raise NotImplementedError
    
    def draw(self, context, canvas, bounds):
        obj = self._create_object(context, canvas.get_ruler())
        
        x, y, w, h = bounds
        
        size = obj.get_minimal_size()
        if w is None:
            w = size[0]
        if h is None:
            h = size[1]
        
        obj.assign_bounds((x, y, w, h))
        obj.draw(canvas, None, None)
