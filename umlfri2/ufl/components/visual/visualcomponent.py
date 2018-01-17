from ..base.component import Component
from .visualobjectcontainer import VisualObjectContainer


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
    
    def create_visual_object(self, context, ruler):
        return VisualObjectContainer(self._create_object(context, ruler))
