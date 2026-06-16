from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from .componentloader import ComponentLoader as ComponentLoader
from .structureloader import UflStructureLoader as UflStructureLoader
from umlfri2.metamodel import ConnectionType as ConnectionType
from umlfri2.metamodel.connectiontypelabel import ConnectionTypeLabel as ConnectionTypeLabel
from umlfri2.types.image import Image as Image
from umlfri2.ufl.components.base.componenttype import ComponentType as ComponentType
from umlfri2.ufl.components.connectionvisual import ConnectionVisualContainerComponent as ConnectionVisualContainerComponent
from umlfri2.ufl.components.visual import VisualContainerComponent as VisualContainerComponent
from umlfri2.ufl.types.complex import UflProportionType as UflProportionType

class ConnectionTypeLoader:
    def __init__(self, storage, xmlroot, file_name) -> None: ...
    def load(self): ...
