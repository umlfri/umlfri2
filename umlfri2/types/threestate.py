class MaybeType:
    def __new__(cls, *args, **kwargs):
        raise Exception("Cannot create a new MaybeType instance")

    def __str__(self):
        return "Maybe"
    
    def __repr__(self):
        return "Maybe"
    
    def __and__(self, other):
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is self:
            return self
        else:
            return other
    
    def __rand__(self, other):
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is self:
            return self
        else:
            return other

    def __or__(self, other):
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is True:
            return True
        else:
            return self

    def __ror__(self, other):
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is True:
            return True
        else:
            return self

    
Maybe = object.__new__(MaybeType)
