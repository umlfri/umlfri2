from ..base.component import Component


class TextComponent(Component):
    def is_control(self):
        return False
    
    def get_text(self, context):
        raise NotImplementedError
