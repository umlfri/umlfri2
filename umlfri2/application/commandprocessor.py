MAX_STACK_SIZE = 100


class CommandProcessor:
    def __init__(self, application):
        self.__undo_stack = []
        self.__redo_stack = []
        self.__application = application
    
    def execute(self, command):
        command.do(self.__application.ruler)
        
        if not command.has_error:
            self.__redo_stack = []
            
            self.__undo_stack.append(command)
            del self.__undo_stack[:-MAX_STACK_SIZE]
            
            self.__application.event_dispatcher.dispatch_all(command.get_updates())
            self.__application.event_dispatcher.dispatch_all(command.get_actions())
    
    def undo(self, count=1):
        for i in range(count):
            command = self.__undo_stack.pop()
            command.undo(self.__application.ruler)
            self.__redo_stack.append(command)
            for event in command.get_updates():
                opposite = event.get_opposite()
                if opposite is not None:
                    self.__application.event_dispatcher.dispatch(opposite)
            
    def redo(self, count=1):
        for i in range(count):
            command = self.__redo_stack.pop()
            command.redo(self.__application.ruler)
            self.__undo_stack.append(command)
            self.__application.event_dispatcher.dispatch_all(command.get_updates())
    
    def clear_buffers(self):
        self.__undo_stack = []
        self.__redo_stack = []
    
    @property
    def undo_stack(self):
        yield from self.__undo_stack
    
    @property
    def redo_stack(self):
        yield from self.__redo_stack
    
    @property
    def can_undo(self):
        if self.__undo_stack:
            return True
        else:
            return False
    
    @property
    def can_redo(self):
        if self.__redo_stack:
            return True
        else:
            return False
    
    @property
    def is_empty(self):
        return not self.__undo_stack and not self.__redo_stack
