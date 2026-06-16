from enum import Enum
from typing import Optional


class AddOnDependencyType(Enum):
    starter = 1
    interface = 2

class AddOnDependency:
    def __init__(
        self,
        type: AddOnDependencyType,
        id: str,
        version: None = None
    ) -> None: ...
    @property
    def type(self): ...
    @property
    def id(self): ...
    @property
    def version(self): ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: AddOnDependency) -> bool: ...
