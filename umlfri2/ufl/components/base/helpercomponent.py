from .component import Component


class HelperComponent(Component):
    def get_children(self, context):
        return self._get_children(context)
