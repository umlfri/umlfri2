from .component import Component


class HelperComponent(Component):
    IS_HELPER = True
    
    def get_children(self, context):
        return self._get_children(context)
