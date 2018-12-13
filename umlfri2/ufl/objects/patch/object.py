from .patch import UflPatch


class UflObjectPatch(UflPatch):
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
        
        def make_reverse(self):
            return UflObjectPatch.AttributeChanged(self.__name, self.__new_value, self.__old_value)
        
        def debug_print(self, file, level):
            print('\t' * level + '=', self.__name, repr(self.__old_value), '=>' , repr(self.__new_value), file=file)
    
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
        
        def make_reverse(self):
            return UflObjectPatch.AttributePatch(self.__name, self.__patch.make_reverse())
        
        def debug_print(self, file, level):
            print('\t' * level + '#', self.__name, file=file)
            self.__patch.debug_print(file, level + 1)
