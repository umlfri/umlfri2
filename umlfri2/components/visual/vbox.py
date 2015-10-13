from .visualcomponent import VisualComponent


class VBox(VisualComponent):
    def get_size(self, context, ruler):
        w = 0
        h = 0
        
        for local, child in self._get_children(context):
            w_child, h_child = child.get_size(local, ruler)
            if w_child > w:
                w = w_child
            h += h_child
        
        return w, h
    
    def draw(self, context, canvas, bounds, shadow = None):
        x, y, w, h = bounds
        
        children = list(self._get_children(context))
        
        h_inner = 0
        w_inner = 0
        h_all = []
        
        for local, child in children:
            w_child, h_child = child.get_size(local, canvas.get_ruler())
            if w_child > w_inner:
                w_inner = w_child
            h_inner += h_child
            h_all.append(h_child)
        
        if w is None:
            w = w_inner
        
        for h_child, (local, child) in zip(h_all, children):
            child.draw(local, canvas, (x, y, w, h_child), shadow)
            y += h_child
