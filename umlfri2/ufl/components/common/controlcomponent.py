from ..base.component import Component


class ControlComponent(Component):
    IS_CONTROL = True
    
    def filter_children(self, context):
        raise NotImplementedError
