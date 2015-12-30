class MaybeType:
    def __str__(self):
        return "Maybe"
    
    def __repr__(self):
        return "Maybe"
    
    def __and__(self, other):
        if other is self:
            return self
        else:
            return other
    
    def __rand__(self, other):
        if other is self:
            return self
        else:
            return other

    
Maybe = MaybeType()
