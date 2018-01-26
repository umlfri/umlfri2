from .type import UflType


class UflLambdaType(UflType):
    # TODO
    def __init__(self, argument_types, return_type):
        self.__argument_types = argument_types
        self.__return_type = return_type
