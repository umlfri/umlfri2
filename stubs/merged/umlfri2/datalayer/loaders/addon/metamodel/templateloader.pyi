from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from umlfri2.metamodel.projecttemplate import ConnectionTemplate as ConnectionTemplate, ConnectionVisualTemplate as ConnectionVisualTemplate, DiagramTemplate as DiagramTemplate, DiagramTemplateState as DiagramTemplateState, ElementTemplate as ElementTemplate, ElementVisualTemplate as ElementVisualTemplate, ProjectTemplate as ProjectTemplate
from umlfri2.types.geometry import Point as Point, Size as Size

class TemplateLoader:
    def __init__(self, xmlroot) -> None: ...
    def load(self): ...
