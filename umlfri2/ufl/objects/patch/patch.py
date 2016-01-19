class UflPatch:
    def __init__(self, type, changes):
        self.__type = type
        self.__changes = changes
    
    def __iter__(self):
        yield from self.__changes
    
    @property
    def type(self):
        return self.__type
    
    @property
    def has_changes(self):
        return len(self.__changes) > 0
    
    def make_reverse(self):
        return self.__class__(self.__type, [change.make_reverse() for change in reversed(self.__changes)])
    
    def get_lonely_change(self):
        if len(self.__changes) == 1:
            return self.__changes[0]
        else:
            return None
