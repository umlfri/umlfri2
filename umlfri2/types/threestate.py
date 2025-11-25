from __future__ import annotations

from typing import Union


class MaybeType:
    def __new__(cls, *args: object, **kwargs: object) -> MaybeType:
        raise Exception("Cannot create a new MaybeType instance")

    def __str__(self) -> str:
        return "Maybe"
    
    def __repr__(self) -> str:
        return "Maybe"
    
    def __and__(self, other: object) -> Union[bool, MaybeType]:
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is self:
            return self
        else:
            return other
    
    def __rand__(self, other: object) -> Union[bool, MaybeType]:
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is self:
            return self
        else:
            return other

    def __or__(self, other: object) -> Union[bool, MaybeType]:
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is True:
            return True
        else:
            return self

    def __ror__(self, other: object) -> Union[bool, MaybeType]:
        if not isinstance(other, (bool, MaybeType)):
            return NotImplemented

        if other is True:
            return True
        else:
            return self

    
Maybe: MaybeType = object.__new__(MaybeType)
