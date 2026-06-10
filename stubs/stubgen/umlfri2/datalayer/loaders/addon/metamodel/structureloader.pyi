from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE
from .componentloader import ComponentLoader as ComponentLoader
from umlfri2.ufl.components.base.componenttype import ComponentType as ComponentType
from umlfri2.ufl.components.text import TextContainerComponent as TextContainerComponent
from umlfri2.ufl.context import TypeContext as TypeContext
from umlfri2.ufl.types.basic import UflIntegerType as UflIntegerType, UflStringType as UflStringType
from umlfri2.ufl.types.structured import UflObjectAttribute as UflObjectAttribute, UflObjectType as UflObjectType
from umlfri2.ufl.types.typeparser import UflTypeParser as UflTypeParser

class UflStructureLoader:
    def __init__(self, xmlroot, file_name) -> None: ...
    def load(self): ...
