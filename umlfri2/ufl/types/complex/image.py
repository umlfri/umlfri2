from umlfri2.types.image import Image
from umlfri2.ufl.types.base.type import UflType


class UflImageType(UflType):
    def __init__(self, default=None):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    @property
    def has_default(self):
        return True
    
    def build_default(self, generator):
        return self.__default
    
    def parse(self, value):
        raise NotImplementedError
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, Image)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return "Image"
