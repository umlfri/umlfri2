from .list import UflListType
from .string import UflStringType
from .flags import UflFlagsType
from .type import UflType


class UflIterableType(UflType):
    def __init__(self, item_type):
        self.__item_type = item_type

    @property
    def item_type(self):
        return self.__item_type

    def is_same_as(self, other):
        if isinstance(other, (UflListType, UflFlagsType)):
            return self.__item_type.is_same_as(other.item_type)
        else:
            return False

    def __str__(self):
        return "Iterable<{0}>".format(self.__item_type)
