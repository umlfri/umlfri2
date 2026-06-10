from typing import List
from umlfri2.application.drawingarea.actions.action import ActionMenuItem
from umlfri2.application.drawingarea.drawingarea import DrawingArea


class ActionMenu:
    def __init__(
        self,
        drawing_area: DrawingArea,
        menu: List[ActionMenuItem]
    ) -> None: ...
    def do(self) -> None: ...
