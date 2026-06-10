from ....constants import ADDON_NAMESPACE as ADDON_NAMESPACE, ADDON_SCHEMA as ADDON_SCHEMA
from umlfri2.types.geometry import PathBuilder as PathBuilder, Point as Point, Size as Size
from umlfri2.ufl.components.connectionvisual.arrow import ArrowDefinition as ArrowDefinition
from umlfri2.ufl.components.visual.rectangle import CornerDefinition as CornerDefinition, SideDefinition as SideDefinition

class DefinitionsLoader:
    def __init__(self, xmlroot) -> None: ...
    def load(self): ...
