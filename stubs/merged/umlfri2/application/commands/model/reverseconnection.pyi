from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.model import ConnectionChangedEvent as ConnectionChangedEvent
from typing import Iterator
from umlfri2.application.events.model.connectionchanged import ConnectionChangedEvent
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class ReverseConnectionCommand(Command):
    def __init__(self, connection: ConnectionObject) -> None: ...
    @property
    def description(self): ...
    def get_updates(self) -> Iterator[ConnectionChangedEvent]: ...
