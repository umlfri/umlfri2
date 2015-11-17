class UflImmutable:
    @property
    def type(self):
        raise NotImplementedError
    
    def make_mutable(self):
        raise NotImplementedError
    
    def apply_patch(self, patch):
        raise NotImplementedError
