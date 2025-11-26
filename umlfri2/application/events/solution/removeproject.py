from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Project


class RemoveProjectEvent(Event):
    def __init__(self, project: Project) -> None:
        self.__project = project
    
    @property
    def project(self) -> Project:
        return self.__project
    
    def get_opposite(self) -> OpenProjectEvent:
        from .openproject import OpenProjectEvent
        
        return OpenProjectEvent(self.__project)
