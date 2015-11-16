class UflListPatch:
    class ItemAdded:
        def __init__(self, index, new_value):
            self.__index = index
            self.__new_value = new_value
        
        @property
        def index(self):
            return self.__index
        
        @property
        def new_value(self):
            return self.__new_value
        
        def make_reverse(self):
            return UflListPatch.ItemRemoved(self.__index, self.__new_value)
    
    class ItemRemoved:
        def __init__(self, index, old_value):
            self.__index = index
            self.__old_value = old_value
        
        @property
        def index(self):
            return self.__index
        
        @property
        def old_value(self):
            return self.__old_value
        
        def make_reverse(self):
            return UflListPatch.ItemAdded(self.__index, self.__old_value)
    
    class ItemPatch:
        def __init__(self, index, patch):
            self.__index = index
            self.__patch = patch
        
        @property
        def index(self):
            return self.__index
        
        @property
        def patch(self):
            return self.__patch
        
        def make_reverse(self):
            return UflListPatch.ItemPatch(self.__index, self.__patch.make_reverse())
    
    def __init__(self, type, changes):
        self.__type = type
        self.__changes = changes
    
    def __iter__(self):
        yield from self.__changes
    
    @property
    def type(self):
        return self.__type
    
    def has_changes(self):
        return len(self.__changes) > 0
    
    def make_reverse(self):
        return UflListPatch(self.__type, [change.make_reverse() for change in self.__changes])
    
    def get_lonely_change(self):
        if len(self.__changes) == 1:
            return self.__changes[0]
