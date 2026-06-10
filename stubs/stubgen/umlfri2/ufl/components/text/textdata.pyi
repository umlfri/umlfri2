from .textcomponent import TextComponent as TextComponent
from _typeshed import Incomplete
from umlfri2.ufl.types.basic import UflStringType as UflStringType

class TextDataComponent(TextComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(self, text) -> None: ...
    def compile(self, type_context) -> None: ...
    def get_text(self, context): ...
