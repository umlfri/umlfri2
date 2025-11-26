from __future__ import annotations

from typing import List, TYPE_CHECKING

from .commandnotdone import CommandNotDone

if TYPE_CHECKING:
    from umlfri2.application.events.base import Event
    from umlfri2.ufl.components.visual.canvas import Ruler


class Command:
    __executed = False
    __undone = False
    __error = None
    
    @property
    def has_error(self) -> bool:
        return self.__error
    
    @property
    def description(self) -> str:
        raise NotImplementedError
    
    def _do(self, ruler: Ruler) -> None:
        raise NotImplementedError
    
    def _undo(self, ruler: Ruler) -> None:
        raise NotImplementedError
    
    def _redo(self, ruler: Ruler) -> None:
        raise NotImplementedError
    
    def do(self, ruler: Ruler) -> None:
        if self.__executed:
            raise Exception("Cannot execute already executed operation")
        
        try:
            self._do(ruler)
        except CommandNotDone:
            self.__error = True
        except:
            self.__error = True
            raise
        
        self.__executed = True
    
    def undo(self, ruler: Ruler) -> None:
        if self.__error:
            raise Exception("There was an error executing command")
        if not self.__executed:
            raise Exception("Command was not executed yet")
        if self.__undone:
            raise Exception("Command was already undone")
        
        self._undo(ruler)
        self.__undone = True
    
    def redo(self, ruler: Ruler) -> None:
        if self.__error:
            raise Exception("There was an error executing command")
        if not self.__executed:
            raise Exception("Command was not executed yet")
        if not self.__undone:
            raise Exception("Command must be undone in order to be redone")
        
        self._redo(ruler)
        self.__undone = False
    
    def get_updates(self) -> List[Event]:
        return []
