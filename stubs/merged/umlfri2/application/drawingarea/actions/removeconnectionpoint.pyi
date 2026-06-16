from ..drawingareacursor import DrawingAreaCursor as DrawingAreaCursor
from .action import Action as Action
from umlfri2.application.commands.diagram import RemoveConnectionPointCommand as RemoveConnectionPointCommand
from umlfri2.application.drawingarea.drawingareacursor import DrawingAreaCursor
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.types.geometry.point import Point


class RemoveConnectionPointAction(Action):
    def __init__(self, connection: ConnectionVisual, index: int) -> None: ...
    @property
    def cursor(self) -> DrawingAreaCursor: ...
    def mouse_down(self, point: Point) -> None: ...
