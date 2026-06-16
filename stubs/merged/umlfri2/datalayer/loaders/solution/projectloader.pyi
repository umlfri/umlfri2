from ...constants import MODEL_NAMESPACE as MODEL_NAMESPACE, MODEL_SCHEMA as MODEL_SCHEMA
from umlfri2.model import Project as Project
from umlfri2.types.geometry import Point as Point, Size as Size
from umlfri2.types.version import Version as Version
from umlfri2.ufl.types.enum import UflFlagsType as UflFlagsType
from umlfri2.ufl.types.structured import UflListType as UflListType, UflObjectType as UflObjectType

class ProjectLoader:
    def __init__(self, xmlfile_or_xmlroot, ruler, addon_manager, save_version) -> None: ...
    def load(self): ...
