from ..constants import MODEL_NAMESPACE as MODEL_NAMESPACE, MODEL_SCHEMA as MODEL_SCHEMA
from umlfri2.ufl.types.enum import UflFlagsType as UflFlagsType
from umlfri2.ufl.types.structured import UflListType as UflListType, UflObjectType as UflObjectType

class ProjectSaver:
    def __init__(self, storage, path, ruler) -> None: ...
    def save(self, project) -> None: ...
