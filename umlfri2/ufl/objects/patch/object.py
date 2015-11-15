class UflObjectPatch:
    class AttributeChanged:
        def __init__(self, name, old_value, new_value):
            self.__name = name
            self.__old_value = old_value
            self.__new_value = new_value
        
        @property
        def name(self):
            return self.__name
        
        @property
        def old_value(self):
            return self.__old_value
        
        @property
        def new_value(self):
            return self.__new_value
    
    class AttributePatch:
        def __init__(self, name, patch):
            self.__name = name
            self.__patch = patch
        
        @property
        def name(self):
            return self.__name
        
        @property
        def patch(self):
            return self.__patch
    
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
