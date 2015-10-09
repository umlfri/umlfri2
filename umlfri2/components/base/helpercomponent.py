from .component import Component


class HelperComponent(Component):
    def is_control(self):
        return False
    
    def get_children(self, context):
        return self._get_children(context)
