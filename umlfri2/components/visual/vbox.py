from umlfri2.types.geometry import Size, Point
from umlfri2.types.threestate import Maybe
from .box import BoxComponent, BoxObject


class VBoxObject(BoxObject):
    def _new_size(self, size, whole_size, delta):
        return Size(whole_size.width, size.height + delta)
    
    def _new_position(self, position, size):
        return Point(position.x, position.y + size.height)
    
    def _compute_size(self, all_widths, all_heights):
        return Size(max(all_widths), sum(all_heights))
    
    def _get_size_component(self, size):
        return size.height
    
    def _get_default_resizable(self, has_expandable):
        if has_expandable:
            return Maybe, True
        else:
            return Maybe, Maybe
    
    def _combine_resizable(self, ret_x, ret_y, child_x, child_y):
        return ret_x & child_x, ret_y

class VBoxComponent(BoxComponent):
    def __init__(self, children, expand):
        super().__init__(VBoxObject, children, expand)
