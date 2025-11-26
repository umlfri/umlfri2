from __future__ import annotations

from typing import Iterator, List, Optional, TYPE_CHECKING

from .events.application import ChangeStatusChangedEvent

if TYPE_CHECKING:
    from umlfri2.application import Application
    from umlfri2.application.commands.base import Command
    from umlfri2.application.events.base import Event

MAX_STACK_SIZE = 100


class CommandProcessor:
    def __init__(self, application: Application) -> None:
        self.__undo_stack = []
        self.__redo_stack = []
        self.__application = application
        self.__unchanged_command = None
    
    def execute(self, command: Command) -> None:
        changed = self.changed
        
        command.do(self.__application.ruler)
        
        if not command.has_error:
            self.__redo_stack = []
            
            self.__undo_stack.append(command)
            del self.__undo_stack[:-MAX_STACK_SIZE]
            
            self.__application.event_dispatcher.dispatch_all(command.get_updates())
        
        new_changed = self.changed
        if new_changed != changed:
            self.__application.event_dispatcher.dispatch(ChangeStatusChangedEvent(new_changed))
    
    def undo(self, count: int = 1) -> None:
        changed = self.changed
        
        for i in range(count):
            if not self.__undo_stack:
                return
            command = self.__undo_stack.pop()
            command.undo(self.__application.ruler)
            self.__redo_stack.append(command)
            for event in reversed(tuple(command.get_updates())):
                opposite = event.get_opposite()
                if opposite is not None:
                    self.__application.event_dispatcher.dispatch(opposite)
        
        new_changed = self.changed
        if new_changed != changed:
            self.__application.event_dispatcher.dispatch(ChangeStatusChangedEvent(new_changed))
            
    def redo(self, count: int = 1) -> None:
        changed = self.changed
        
        for i in range(count):
            if not self.__redo_stack:
                return
            command = self.__redo_stack.pop()
            command.redo(self.__application.ruler)
            self.__undo_stack.append(command)
            self.__application.event_dispatcher.dispatch_all(command.get_updates())
        
        new_changed = self.changed
        if new_changed != changed:
            self.__application.event_dispatcher.dispatch(ChangeStatusChangedEvent(new_changed))
    
    def clear_buffers(self) -> None:
        self.__undo_stack = []
        self.__redo_stack = []
    
    @property
    def undo_stack_size(self) -> int:
        return len(self.__undo_stack)
    
    def get_undo_stack(self, count: Optional[int] = None) -> Iterator[Command]:
        if count is None:
            yield from reversed(self.__undo_stack)
        else:
            yield from reversed(self.__undo_stack[-count:])
    
    @property
    def redo_stack_size(self) -> int:
        return len(self.__redo_stack)
    
    def get_redo_stack(self, count: Optional[int] = None) -> Iterator[Command]:
        if count is None:
            yield from reversed(self.__redo_stack)
        else:
            yield from reversed(self.__redo_stack[-count:])
    
    @property
    def can_undo(self) -> bool:
        if self.__undo_stack:
            return True
        else:
            return False
    
    @property
    def can_redo(self) -> bool:
        if self.__redo_stack:
            return True
        else:
            return False
    
    @property
    def changed(self) -> bool:
        if self.__undo_stack:
            return self.__unchanged_command is None or self.__undo_stack[-1] is not self.__unchanged_command
        else:
            return self.__unchanged_command is not None
    
    def mark_unchanged(self) -> None:
        if self.__undo_stack:
            self.__unchanged_command = self.__undo_stack[-1]
        else:
            self.__unchanged_command = None
