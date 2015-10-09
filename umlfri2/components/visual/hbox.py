from .visualcomponent import VisualComponent


class HBox(VisualComponent):
    def get_size(self, context, ruler):
        w = 0
        h = 0
        
        for local, child in self._get_children(context):
            w_child, h_child = child.get_size(local, ruler)
            w += w_child
            if h_child > h:
                h = h_child
        
        return w, h
    
    def draw(self, context, canvas, bounds, shadow=None):
        x, y, w, h = bounds
        
        children = list(self._get_children(context))
        
        h_inner = 0
        w_inner = 0
        w_all = []
        
        for local, child in children:
            w_child, h_child = child.get_size(local, canvas.get_ruler())
            w_inner += w_child
            if h_child > h_inner:
                h_inner = h_child
            w_all.append(w_inner)
        
        if h is None:
            h = h_inner
        
        for w_child, (local, child) in zip(w_all, children):
            child.draw(local, canvas, (x, y, w_child, h), shadow)
            x += w_child
