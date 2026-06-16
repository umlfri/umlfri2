from ..base.component import Component as Component

class ControlComponent(Component):
    IS_CONTROL: bool
    def filter_children(self, context) -> None: ...
