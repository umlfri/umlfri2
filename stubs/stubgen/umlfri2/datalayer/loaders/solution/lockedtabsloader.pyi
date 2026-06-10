from ...constants import MODEL_NAMESPACE as MODEL_NAMESPACE, MODEL_SCHEMA as MODEL_SCHEMA
from _typeshed import Incomplete
from typing import NamedTuple

class StartupTab(NamedTuple):
    diagram: Incomplete
    locked: Incomplete

class LockedTabsLoader:
    def __init__(self, xmlroot, all_diagrams) -> None: ...
    def load(self): ...
