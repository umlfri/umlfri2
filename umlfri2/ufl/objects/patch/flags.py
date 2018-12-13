from .patch import UflPatch


class UflFlagsPatch(UflPatch):
    class ItemAdded:
        def __init__(self, new_value):
            self.__new_value = new_value
        
        @property
        def new_value(self):
            return self.__new_value
        
        def make_reverse(self):
            return UflFlagsPatch.ItemRemoved(self.__new_value)
        
        def debug_print(self, file, level):
            print('\t' * level + '+', repr(self.__new_value), file=file)
    
    class ItemRemoved:
        def __init__(self, old_value):
            self.__old_value = old_value
        
        @property
        def old_value(self):
            return self.__old_value
        
        def make_reverse(self):
            return UflFlagsPatch.ItemAdded(self.__old_value)
        
        def debug_print(self, file, level):
            print('\t' * level + '-', repr(self.__old_value), file=file)
