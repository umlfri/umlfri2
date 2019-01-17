from ..base.type import UflType


class UflGenericType(UflType):
    # TODO
    def __init__(self, base_type):
        self.__base_type = base_type
