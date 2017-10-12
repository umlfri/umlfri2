class TypeContext:
    def __init__(self):
        self.__local_types = {}
    
    def get_variable_type(self, name):
        return self.__local_types[name]
    
    def as_dict(self):
        return self.__local_types.copy()
    
    def set_variable_type(self, name, type):
        ret = TypeContext()
        ret.__local_types = self.__local_types.copy()
        ret.__local_types[name] = type
        return ret
