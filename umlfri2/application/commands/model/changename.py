from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING

from umlfri2.application.events.model import ProjectChangedEvent
from ..base import Command, CommandNotDone

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.model import Project


class ChangeProjectNameCommand(Command):
    def __init__(self, project: Project, name: str) -> None:
        self.__project = project
        self.__name = name
        self.__old_name: Optional[str] = None
    
    @property
    def description(self) -> str:
        return "Changed project name to '{0}'".format(self.__name)

    def _do(self, ruler: object) -> None:
        if self.__project.name == self.__name:
            raise CommandNotDone
        self.__old_name = self.__project.name
        self._redo(ruler)

    def _redo(self, ruler: object) -> None:
        self.__project.name = self.__name
    
    def _undo(self, ruler: object) -> None:
        self.__project.name = self.__old_name
    
    def get_updates(self) -> Iterator[Event]:
        yield ProjectChangedEvent(self.__project)
