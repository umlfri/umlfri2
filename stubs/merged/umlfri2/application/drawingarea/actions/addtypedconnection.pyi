from .addconnection import AddConnectionAction as AddConnectionAction
from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand as AddDiagramConnectionCommand
from typing import (
    Any,
    List,
    Union,
)
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.types.geometry.point import Point


class AddTypedConnectionAction(AddConnectionAction):
    def __init__(self, type: str) -> None: ...
    @property
    def connection_type(self): ...
