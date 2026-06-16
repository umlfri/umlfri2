from .component import Component as Component

class HelperComponent(Component):
    IS_HELPER: bool
    def get_children(self, context): ...
