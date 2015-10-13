from ..base.component import Component


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
    
    def get_size(self, context, ruler):
        raise NotImplementedError
    
    def _compute_bounds(self, context, ruler, original_bounds):
        x, y, w, h = original_bounds
        
        w_inner, h_inner = self.get_size(context, ruler)
        
        if w is None:
            w = w_inner
        
        if h is None:
            h = h_inner
        
        return (x, y, w, h), (w_inner, h_inner)
    
    def draw(self, context, canvas, bounds, shadow=None):
        raise NotImplemented
