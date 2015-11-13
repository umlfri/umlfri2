from umlfri2.types.geometry import Size, Rectangle, Point
from .box import BoxObject, BoxComponent


class HBoxObject(BoxObject):
    def _new_size(self, size, whole_size, delta):
        return Size(size.width + delta, whole_size.height)
    
    def _new_position(self, position, size):
        return Point(position.x + size.width, position.y)
    
    def _compute_size(self, all_widths, all_heights):
        return Size(sum(all_widths), max(all_heights))
    
    def _get_size_component(self, size):
        return size.width
    
    def _get_default_resizable(self):
        return True, False

class HBoxComponent(BoxComponent):
    def __init__(self, children, expand):
        super().__init__(HBoxObject, children, expand)
