from .type import UflType


class UflObjectType(UflType):
    def __init__(self, attributes):
        self.__attributes = dict(attributes)
    
    @property
    def attributes(self):
        return self.__attributes.copy()
    
    def get_attribute(self, name):
        return self.__attributes[name]
