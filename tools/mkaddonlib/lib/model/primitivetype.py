class PrimitiveType:
    def __init__(self, name, numeric=False, logic=False, string=False, object=False, default=None, convertor=None):
        self.__name = name
        self.__numeric = numeric
        self.__logic = logic
        self.__string = string
        self.__object = object
        self.__default = default
        self.__convertor = convertor
    
    @property
    def name(self):
        return self.__name
    
    @property
    def fqn(self):
        return '::' + self.__name
    
    @property
    def is_numeric(self):
        return self.__isNumberic
    
    @property
    def is_logic(self):
        return self.__logic
    
    @property
    def is_string(self):
        return self.__string
    
    @property
    def is_object(self):
        return self.__object
    
    @property
    def default(self):
        return self.__default
    
    @property
    def can_convert(self):
        return self.__convertor is not None
    
    def convert(self, value):
        return self.__convertor(value)
    
    @property
    def type_name(self):
        return 'PrimitiveType'

bool_convertor = lambda x: (x == 'true')

PRIMITIVE_TYPES = {
    'boolean':      PrimitiveType('boolean', logic=True, convertor=bool_convertor, default=False),
    'inputstream':  PrimitiveType('inputstream', object=True),
    'int32':        PrimitiveType('int32', numeric=True, convertor=int, default=0),
    'float':        PrimitiveType('float', numeric=True, convertor=int, default=0.0),
    'variant':      PrimitiveType('variant'), # one of: boolean, int32, float, string
    'string':       PrimitiveType('string', string=True, convertor=str, default=""),
    'xy':           PrimitiveType('xy', object=True),
    'xywh':         PrimitiveType('xywh', object=True),
    'wh':           PrimitiveType('wh', object=True),
}
