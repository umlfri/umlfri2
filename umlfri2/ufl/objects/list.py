class UflList:
    def __init__(self, type):
        self.__values = []
        self.__type = type
    
    @property
    def type(self):
        return self.__type
    
    def __iter__(self):
        yield from self.__values
    
    def get_item(self, index):
        return self.__values[index]
    
    def set_item(self, index, value):
        item_type = self.__type.item_type
        
        if item_type.is_immutable and not item_type.is_valid_value(value):
            raise ValueError
        self.__values[index] = value
    
    def get_length(self):
        return len(self.__values)
    
    def append(self):
        value = self.__type.item_type.build_default()
        self.__values.append(value)
        return value
    
    def __bool__(self):
        return bool(self.__values)
