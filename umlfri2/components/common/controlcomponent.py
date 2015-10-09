from ..base.component import Component


class ControlComponent(Component):
    def is_control(self):
        return True
    
    def filter_children(self, context):
        raise NotImplementedError
