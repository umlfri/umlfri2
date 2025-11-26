from __future__ import annotations

from typing import TYPE_CHECKING

from umlfri2.application.events.tabs import TabLockStatusChangedEvent
from .drawingarea import DrawingArea

if TYPE_CHECKING:
    from umlfri2.application import Application
    from umlfri2.application.tablist import TabList
    from umlfri2.model import Diagram
    from umlfri2.types.image import Image


class Tab:
    def __init__(self, application: Application, tabs: TabList, diagram: Diagram, locked: bool = False) -> None:
        self.__tabs = tabs
        self.__application = application
        self.__drawing_area = DrawingArea(application, diagram)
        self.__locked = locked
    
    @property
    def locked(self) -> bool:
        return self.__locked
    
    def lock(self) -> None:
        self.__locked = True
        self.__application.event_dispatcher.dispatch(TabLockStatusChangedEvent(self))
    
    def unlock(self) -> None:
        self.__locked = False
        self.__application.event_dispatcher.dispatch(TabLockStatusChangedEvent(self))
    
    def close(self) -> None:
        self.__tabs._close_tab(self)
    
    @property
    def drawing_area(self) -> DrawingArea:
        return self.__drawing_area
    
    @property
    def name(self) -> str:
        return self.__drawing_area.diagram.get_display_name()
    
    @property
    def icon(self) -> Image:
        return self.__drawing_area.diagram.type.icon
