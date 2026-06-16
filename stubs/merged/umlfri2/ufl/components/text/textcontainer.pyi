from .textcomponent import TextComponent as TextComponent
from typing import Optional
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class TextContainerComponent(TextComponent):
    def get_text(self, context: Context) -> Optional[str]: ...
    def compile(self, type_context: TypeContext) -> None: ...
