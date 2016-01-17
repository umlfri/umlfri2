class KeyValueType:
    def __init__(self, key_type, value_type):
        self.__key_type = key_type
        self.__value_type = value_type
    
    @property
    def fqn(self):
        return "::keyvalue<{0}, {1}>".format(self.__key_type.fqn, self.__value_type.fqn)
    
    @property
    def key_type(self):
        return self.__key_type
    
    @property
    def value_type(self):
        return self.__value_type
    
    @property
    def type_name(self):
        return 'KeyValueType'
