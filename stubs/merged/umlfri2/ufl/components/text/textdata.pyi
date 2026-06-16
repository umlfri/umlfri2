from .textcomponent import TextComponent as TextComponent
from _typeshed import Incomplete
from umlfri2.ufl.types.basic import UflStringType as UflStringType
from typing import Union
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext

class TextDataComponent(TextComponent):
    ATTRIBUTES: Incomplete
    HAS_CHILDREN: bool
    def __init__(
        self,
        text: Union[DynamicValueProvider, ConstantValueProvider]
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def get_text(self, context: Context) -> str: ...
