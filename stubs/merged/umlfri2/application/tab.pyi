from .drawingarea import DrawingArea as DrawingArea
from umlfri2.application.events.tabs import TabLockStatusChangedEvent as TabLockStatusChangedEvent
from umlfri2.application.application import Application
from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.application.tablist import TabList
from umlfri2.model.diagram import Diagram
from umlfri2.types.image import Image


class Tab:
    def __init__(
        self,
        application: Application,
        tabs: TabList,
        diagram: Diagram,
        locked: bool = False
    ) -> None: ...
    @property
    def locked(self) -> bool: ...
    def lock(self) -> None: ...
    def unlock(self) -> None: ...
    def close(self) -> None: ...
    @property
    def drawing_area(self) -> DrawingArea: ...
    @property
    def name(self) -> str: ...
    @property
    def icon(self) -> Image: ...
