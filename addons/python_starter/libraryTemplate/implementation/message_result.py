from base64 import b64decode
from io import BytesIO


def _inputstream(data):
    return BytesIO(b64decode(data))


class MessageResult:
    def __init__(self, factory, data):
        self.__factory = factory
        self.__data = data
    
    def throws_exception(self, name, exception):
        if 'exception' in self.__data and self.__data['exception']['type'] == name:
            raise exception()
        return self
    
    def check_unknown_exceptions(self):
        if 'exception' in self.__data:
            raise Exception("Unknown exception {0}".format(self.__data['exception']['type']))
        
        return self
    
    def __control_null(self, allow_null):
        return allow_null and 'return' not in self.__data
    
    def return_void(self):
        pass
        
    def return_boolean(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return bool(self.__data['return'])
        
    def return_inputstream(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return _inputstream(self.__data['return'])
    
    def return_int32(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return int(self.__data['return'])
    
    def return_float(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return float(self.__data['return'])
    
    def return_variant(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return self.__data['return']
    
    def return_string(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return str(self.__data['return'])
    
    def return_xy(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return (int(self.__data['return'][0]), int(self.__data['return'][1]))
    
    def return_xywh(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return (int(self.__data['return'][0]), int(self.__data['return'][1]), int(self.__data['return'][2]),
                int(self.__data['return'][3]))
    
    def return_wh(self, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        return (int(self.__data['return'][0]), int(self.__data['return'][1]))
    
    def return_object(self, type, allow_null=False):
        if self.__control_null(allow_null):
            return None
        
        if 'return' not in self.__data:
            return None
        
        if type is None:
            return self.__factory.get_instance(self.__data['return'][0], self.__data['return'][1])
        else:
            return self.__factory.get_instance(type, self.__data['return'])
        
    def iterate_boolean(self):
        for item in self.__data['return']:
            yield bool(item)
    
    def iterate_int32(self):
        for item in self.__data['return']:
            yield int(item)
    
    def iterate_float(self):
        for item in self.__data['return']:
            yield float(item)
    
    def iterate_variant(self):
        for item in self.__data['return']:
            yield item
    
    def iterate_string(self):
        for item in self.__data['return']:
            yield str(item)
    
    def iterate_xy(self):
        for item in self.__data['return']:
            yield (int(item[0]), int(item[1]))
    
    def iterate_xywh(self):
        for item in self.__data['return']:
            yield (int(item[0]), int(item[1]), int(item[2]), int(item[3]))
    
    def iterate_wh(self):
        for item in self.__data['return']:
            yield (int(item[0]), int(item[1]))
    
    def iterate_keyvalue_string_variant(self):
        for key, value in self.__data['return']:
            yield (str(key), value)
    
    def iterate_object(self, type):
        for item in self.__data['return']:
            if type is None:
                yield self.__factory.get_instance(item[0], item[1])
            else:
                yield self.__factory.get_instance(type, item)
