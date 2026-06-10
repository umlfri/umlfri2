from typing import Optional
from umlfri2.application.drawingarea.drawingarea import DrawingArea


class ToolBox:
    def __init__(
        self,
        drawing_area: Optional[DrawingArea],
        show_names: bool
    ) -> None: ...
    @property
    def drawing_area(self) -> None: ...
