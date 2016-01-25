class UflImmutable:
    @property
    def type(self):
        raise NotImplementedError
    
    def make_mutable(self):
        raise NotImplementedError
    
    def apply_patch(self, patch):
        raise NotImplementedError
    
    def copy(self):
        raise NotImplementedError
    
    def __eq__(self, other):
        raise NotImplementedError
    
    def __ne__(self, other):
        return not self.__eq__(other)
