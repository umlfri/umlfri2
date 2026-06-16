from ..base.type import UflType as UflType

from umlfri2.ufl.types.generic.generic import UflGenericType

class UflTypeIdentifierType(UflType):
    def __init__(self, generic: UflGenericType) -> None: ...
