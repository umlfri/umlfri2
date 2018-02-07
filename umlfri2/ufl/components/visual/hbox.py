from umlfri2.types.geometry import Size, Point
from umlfri2.types.threestate import Maybe
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
    
    def _combine_resizable(self, ret_x, ret_y, child_x, child_y, expand):
        if expand:
            child_x = True
        return ret_x | child_x, ret_y & child_y

class HBoxComponent(BoxComponent):
    def __init__(self, children, expand):
        super().__init__(HBoxObject, children, expand)
