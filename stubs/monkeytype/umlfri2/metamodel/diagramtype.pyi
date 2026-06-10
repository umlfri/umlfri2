from typing import (
    Tuple,
    Union,
)
from umlfri2.metamodel.connectiontype import ConnectionType
from umlfri2.metamodel.elementtype import ElementType
from umlfri2.metamodel.metamodel import Metamodel
from umlfri2.model.diagram import Diagram
from umlfri2.types.color import Color
from umlfri2.types.image import Image
from umlfri2.ufl.components.text.textcontainer import TextContainerComponent
from umlfri2.ufl.components.valueproviders.constant import ConstantValueProvider
from umlfri2.ufl.components.valueproviders.dynamic import DynamicValueProvider
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.structured.object import UflObjectType


class DiagramType:
    def __init__(
        self,
        id: str,
        icon: Image,
        ufl_type: UflObjectType,
        display_name: TextContainerComponent,
        element_types: Union[Tuple[ElementType, ElementType, ElementType, ElementType, ElementType, ElementType, ElementType], Tuple[ElementType, ElementType, ElementType, ElementType], Tuple[ElementType, ElementType, ElementType]],
        connection_types: Union[Tuple[ConnectionType, ConnectionType], Tuple[ConnectionType], Tuple[ConnectionType, ConnectionType, ConnectionType], Tuple[ConnectionType, ConnectionType, ConnectionType, ConnectionType, ConnectionType]],
        background_color: Union[DynamicValueProvider, ConstantValueProvider]
    ) -> None: ...
    def _set_metamodel(self, metamodel: Metamodel) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    @property
    def connection_types(
        self
    ) -> Union[Tuple[ConnectionType, ConnectionType, ConnectionType, ConnectionType, ConnectionType], Tuple[ConnectionType, ConnectionType], Tuple[ConnectionType]]: ...
    @property
    def element_types(
        self
    ) -> Union[Tuple[ElementType, ElementType, ElementType, ElementType, ElementType, ElementType, ElementType], Tuple[ElementType, ElementType, ElementType]]: ...
    def get_background_color(self, diagram: Diagram) -> Color: ...
    def get_display_name(self, diagram: Diagram) -> str: ...
    @property
    def icon(self) -> Image: ...
    @property
    def id(self) -> str: ...
    @property
    def metamodel(self) -> Metamodel: ...
    @property
    def ufl_type(self) -> UflObjectType: ...
