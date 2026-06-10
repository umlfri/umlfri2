from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple
from umlfri2.application.events.diagram import ConnectionHiddenEvent as ConnectionHiddenEvent, ElementHiddenEvent as ElementHiddenEvent

class HiddenVisualDescription(NamedTuple):
    z_order: Incomplete
    visual: Incomplete

class HideElementsCommand(Command):
    def __init__(self, diagram, elements) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Generator[Incomplete]: ...
