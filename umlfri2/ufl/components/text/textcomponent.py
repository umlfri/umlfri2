from ..base.component import Component


class TextComponent(Component):
    def get_text(self, context):
        raise NotImplementedError
