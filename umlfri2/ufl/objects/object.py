class UflObject:
    def __init__(self, type, attributes):
        self.__type = type
        self.__attributes = attributes
    
    @property
    def type(self):
        return self.__type
    
    def get_values(self):
        yield from self.__attributes.items()
    
    def get_value(self, name):
        return self.__attributes[name]
    
    def set_value(self, name, value):
        attribute_type = self.__type.get_attribute_type(name)
        
        if attribute_type.is_immutable and  not attribute_type.is_valid_value(value):
            raise ValueError
        
        self.__attributes[name] = value
