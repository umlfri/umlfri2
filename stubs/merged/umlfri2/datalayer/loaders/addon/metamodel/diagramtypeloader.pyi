from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from .componentloader import ComponentLoader as ComponentLoader
from .structureloader import UflStructureLoader as UflStructureLoader
from umlfri2.metamodel import DiagramType as DiagramType
from umlfri2.types.image import Image as Image
from umlfri2.ufl.components.base.componenttype import ComponentType as ComponentType
from umlfri2.ufl.components.text import TextContainerComponent as TextContainerComponent
from umlfri2.ufl.components.valueproviders import ConstantValueProvider as ConstantValueProvider, DynamicValueProvider as DynamicValueProvider

class DiagramTypeLoader:
    def __init__(self, storage, xmlroot, file_name, elements, connections) -> None: ...
    def load(self): ...
