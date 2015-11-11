class CommandNotDone(Exception):
    pass


class Command:
    __executed = False
    __undone = False
    __error = None
    
    @property
    def has_error(self):
        return self.__error
    
    def _execute(self):
        raise NotImplementedError
    
    def _undo(self):
        raise NotImplementedError
    
    def _redo(self):
        raise NotImplementedError
    
    def execute(self):
        if self.__executed:
            raise Exception("Cannot execute already executed operation")
        
        try:
            self._execute()
        except CommandNotDone:
            self.__error = True
        except:
            self.__error = True
            raise
        
        self.__executed = True
    
    def undo(self):
        if self.__error:
            raise Exception("There was an error executing command")
        if not self.__executed:
            raise Exception("Command was not executed yet")
        if self.__undone:
            raise Exception("Command was already undone")
        
        self._undo()
        self.__undone = True
    
    def redo(self):
        if self.__error:
            raise Exception("There was an error executing command")
        if not self.__executed:
            raise Exception("Command was not executed yet")
        if not self.__undone:
            raise Exception("Command must be undone in order to be redone")
        
        self._redo()
        self.__undone = False
    
    def get_updates(self):
        return []
    
    def get_actions(self):
        return []
