from .checkdata import check_any as check_any
from _typeshed import Incomplete
from collections.abc import Generator
from enum import Enum

class DiagramTemplateState(Enum):
    closed = 1
    opened = 2
    locked = 3

class DiagramTemplate:
    def __init__(self, type, data, elements, connections, parent_id, state=...) -> None: ...
    @property
    def type(self): ...
    @property
    def data(self): ...
    @property
    def elements(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def connections(self) -> Generator[Incomplete, Incomplete]: ...
    @property
    def parent_id(self): ...
    @property
    def state(self): ...
