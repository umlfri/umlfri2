from ...constants import MODEL_NAMESPACE as MODEL_NAMESPACE, MODEL_SCHEMA as MODEL_SCHEMA
from _typeshed import Incomplete
from typing import NamedTuple

class ProjectInfo(NamedTuple):
    id: Incomplete

class SolutionInfo(NamedTuple):
    id: Incomplete
    projects: Incomplete

class SolutionInfoLoader:
    def __init__(self, xmlroot) -> None: ...
    def load(self): ...
