from __future__ import annotations

import os.path
from typing import TYPE_CHECKING

from .events.application import RecentFilesChangedEvent

if TYPE_CHECKING:
    from umlfri2.application import Application
    from umlfri2.application.recentfiles import RecentFiles


class RecentFile:
    def __init__(self, application: Application, recent_files: RecentFiles, file_path: str,
                 pinned: bool = False) -> None:
        self.__application = application
        self.__recent_files = recent_files
        
        self.__pinned = pinned
        
        self.__file_path = file_path
    
    @property
    def exists(self) -> bool:
        return os.path.exists(self.__file_path)
    
    @property
    def file_name(self) -> str:
        return os.path.basename(self.__file_path)
    
    @property
    def path(self) -> str:
        return self.__file_path
    
    @property
    def pinned(self) -> bool:
        return self.__pinned
    
    def pin(self) -> None:
        if not self.__pinned:
            self.__pinned = True
            self.__recent_files._pin_changed(self)
            self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(self.__file_path))

    def unpin(self) -> None:
        if self.__pinned:
            self.__pinned = False
            self.__recent_files._pin_changed(self)
            self.__application.event_dispatcher.dispatch(RecentFilesChangedEvent(self.__file_path))
    
    def remove(self) -> None:
        self.__recent_files._remove(self)
    
    def open(self) -> None:
        self.__application.open_solution(self.__file_path)
