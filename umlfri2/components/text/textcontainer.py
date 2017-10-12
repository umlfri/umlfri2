from .textcomponent import TextComponent


class TextContainerComponent(TextComponent):
    def get_text(self, context):
        children = list(self._get_children(context))
        if children:
            return "".join(child.get_text(local) for local, child in children)
        else:
            return None
    
    def compile(self, type_context):
        self._compile_children(type_context)
