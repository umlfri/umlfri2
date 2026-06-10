from typing import Optional
from umlfri2.metamodel.defaultelementaction import DefaultElementAction
from umlfri2.metamodel.metamodel import Metamodel
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.image import Image
from umlfri2.ufl.components.text.textcontainer import TextContainerComponent
from umlfri2.ufl.components.visual.visualcontainer import (
    VisualContainerComponent,
    VisualObjectContainer,
)
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType


class ElementType:
    def __init__(
        self,
        id: str,
        icon: Image,
        ufl_type: UflObjectType,
        display_name: TextContainerComponent,
        appearance: VisualContainerComponent,
        default_action: DefaultElementAction,
        node_access_depth: ElementAccessDepth,
        allow_direct_add: bool
    ) -> None: ...
    def _set_metamodel(self, metamodel: Metamodel) -> None: ...
    @property
    def allow_direct_add(self) -> bool: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def create_appearance_object(
        self,
        element: ElementObject,
        ruler: QTRuler
    ) -> VisualObjectContainer: ...
    @property
    def default_action(self) -> DefaultElementAction: ...
    def get_display_name(self, element: ElementObject) -> Optional[str]: ...
    @property
    def icon(self) -> Image: ...
    @property
    def id(self) -> str: ...
    @property
    def metamodel(self) -> Metamodel: ...
    @property
    def node_access_depth(self) -> ElementAccessDepth: ...
    @property
    def ufl_type(self) -> UflObjectType: ...


class NodeMetadata:
    @staticmethod
    def build_node_metadata_types(
        element_type: Optional[ElementType] = ...
    ) -> UflVariableWithMetadataType: ...
