from .enum import UflEnumType


class UflStringEnumType(UflEnumType):
    @property
    def default(self):
        return self.default_item
    
    def build_default(self, generator):
        return self.default_item
    
    def parse(self, value):
        if not self.is_valid_item(value):
            raise ValueError("Invalid value")
        return value
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        return self.possibilities == other.possibilities
    
    def is_valid_value(self, value):
        return self.is_valid_item(value)
    
    def is_default_value(self, value):
        return self.default_item == value
    
    def __str__(self):
        return 'Enum[{0}]'.format(", ".join(self.__possibilities))
