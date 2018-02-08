from ..base.component import Component


class VisualObject:
    def assign_bounds(self, bounds):
        raise NotImplementedError
    
    def get_minimal_size(self):
        raise NotImplementedError
    
    def draw(self, canvas, shadow):
        raise NotImplementedError
    
    def is_resizable(self):
        raise NotImplementedError


class VisualComponent(Component):
    def _create_object(self, context, ruler):
        raise NotImplementedError
