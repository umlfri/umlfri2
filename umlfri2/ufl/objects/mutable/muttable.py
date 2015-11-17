class UflMutable:
    @property
    def type(self):
        raise NotImplementedError
    
    def make_immutable(self):
        raise NotImplementedError
    
    def make_patch(self):
        raise NotImplementedError
