from ..base.helpercomponent import HelperComponent as HelperComponent
from .controlcomponent import ControlComponent as ControlComponent
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.ufl.types.generic import UflAnyType as UflAnyType
from typing import (
    Iterator,
    List,
    Tuple,
    Union,
)
from umlfri2.ufl.components.connectionvisual.arrow import ConnectionArrowComponent
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.components.visual.sizer import SizerComponent
from umlfri2.ufl.components.visual.textbox import TextBoxComponent
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType

class SwitchCaseComponent(HelperComponent):
    ATTRIBUTES: Incomplete
    def __init__(
        self,
        children: List[Union[TextBoxComponent, ConnectionArrowComponent, SizerComponent]],
        value: ConstantValueProvider
    ) -> None: ...
    def get_value(self, context: Context) -> str: ...
    def retype(self, type: UflStringEnumType) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...

class SwitchDefaultComponent(HelperComponent):
    def compile(self, type_context) -> None: ...

class SwitchComponent(ControlComponent):
    ATTRIBUTES: Incomplete
    SPECIAL_CHILDREN: Incomplete
    ONLY_SPECIAL_CHILDREN: bool
    def __init__(
        self,
        children: List[SwitchCaseComponent],
        value: DynamicValueProvider
    ) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def filter_children(
        self,
        context: Context
    ) -> Iterator[Union[Tuple[Context, ConnectionArrowComponent], Tuple[Context, TextBoxComponent]]]: ...
