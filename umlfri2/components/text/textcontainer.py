from .textcomponent import TextComponent


class TextContainer(TextComponent):
    def get_text(self, context):
        return "".join(child.get_text(local) for local, child in self._get_children(context))
