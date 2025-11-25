from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Project


class OpenProjectEvent(Event):
    def __init__(self, project: Project) -> None:
        self.__project = project
    
    @property
    def project(self) -> Project:
        return self.__project
    
    def get_opposite(self) -> RemoveProjectEvent:
        from .removeproject import RemoveProjectEvent
        
        return RemoveProjectEvent(self.__project)
