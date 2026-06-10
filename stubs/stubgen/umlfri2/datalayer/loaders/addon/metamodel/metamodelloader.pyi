from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE
from .connectiontypeloader import ConnectionTypeLoader as ConnectionTypeLoader
from .definitionsloader import DefinitionsLoader as DefinitionsLoader
from .diagramtypeloader import DiagramTypeLoader as DiagramTypeLoader
from .elementtypeloader import ElementTypeLoader as ElementTypeLoader
from .structureloader import UflStructureLoader as UflStructureLoader
from .templateloader import TemplateLoader as TemplateLoader
from .translationloader import TranslationLoader as TranslationLoader
from umlfri2.metamodel import Metamodel as Metamodel

class MetamodelLoader:
    def __init__(self, storage, addon_storage, addon_info) -> None: ...
    def load(self): ...
