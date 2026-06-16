from .action import ActionMenuItem as ActionMenuItem
from .addconnection import AddConnectionAction as AddConnectionAction
from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand as AddDiagramConnectionCommand
from typing import (
    Any,
    List,
    Optional,
)
from umlfri2.application.drawingarea.actions.action import ActionMenuItem
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.types.geometry.point import Point


class AddUntypedConnectionAction(AddConnectionAction):
    def __init__(self, source_element: ElementVisual) -> None: ...
    @property
    def menu_to_show(self) -> Optional[List[ActionMenuItem]]: ...
