from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from .componentloader import ComponentLoader as ComponentLoader
from .structureloader import UflStructureLoader as UflStructureLoader
from umlfri2.metamodel import DefaultElementAction as DefaultElementAction, ElementAccessDepth as ElementAccessDepth, ElementType as ElementType
from umlfri2.types.image import Image as Image
from umlfri2.ufl.components.base.componenttype import ComponentType as ComponentType
from umlfri2.ufl.components.text import TextContainerComponent as TextContainerComponent
from umlfri2.ufl.components.visual import VisualContainerComponent as VisualContainerComponent

class ElementTypeLoader:
    def __init__(self, storage, xmlroot, file_name) -> None: ...
    def load(self): ...
