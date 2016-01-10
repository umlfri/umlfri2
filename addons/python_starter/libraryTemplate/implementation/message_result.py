from base64 import b64decode
from io import BytesIO


class MessageResult:
    def __init__(self, factory, data):
        self.__factory = factory
        self.__data = data
    
    def throws_exception(self, name, exception):
        if 'exception' in self.__data and self.__data['exception']['type'] == name:
            raise exception()
        return self
    
    def __control_exception(self):
        if 'exception' in self.__data:
            raise Exception("Unknown exception {0}".format(self.__data['exception']['type']))
    
    def return_void(self):
        self.__control_exception()
        
    def return_boolean(self):
        self.__control_exception()
        
        return bool(self.__data['return'])
        
    def return_inputstream(self):
        self.__control_exception()
        
        return BytesIO(b64decode(self.__data['return']))
    
    def return_int32(self):
        self.__control_exception()
        
        return int(self.__data['return'])
    
    def return_float(self):
        self.__control_exception()
        
        return float(self.__data['return'])
    
    def return_variant(self):
        self.__control_exception()
        
        return self.__data['return']
    
    def return_string(self):
        self.__control_exception()
        
        return self.__data['return']
    
    def return_xy(self):
        self.__control_exception()
        
        return (int(self.__data['return'][0]), int(self.__data['return'][1]))
    
    def return_xywh(self):
        self.__control_exception()
        
        return (int(self.__data['return'][0]), int(self.__data['return'][1]), int(self.__data['return'][2]),
                int(self.__data['return'][3]))
    
    def return_wh(self):
        self.__control_exception()
        
        return (int(self.__data['return'][0]), int(self.__data['return'][1]))
    
    def return_keyvalue(self):
        self.__control_exception()
        
        return (str(self.__data['return'][0]), self.__data['return'][1])
    
    def return_object(self, type):
        self.__control_exception()
        
        if 'return' not in self.__data:
            return None
        
        if type is None:
            return self.__factory.get_instance(self.__data['return'][0], self.__data['return'][1])
        else:
            return self.__factory.get_instance(type, self.__data['return'])
        
    def iterate_boolean(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield bool(item)
    
    def iterate_int32(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield int(item)
    
    def iterate_float(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield float(item)
    
    def iterate_variant(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield item
    
    def iterate_string(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield item
    
    def iterate_xy(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield (int(item[0]), int(item[1]))
    
    def iterate_xywh(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield (int(item[0]), int(item[1]), int(item[2]), int(item[3]))
    
    def iterate_wh(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield (int(item[0]), int(item[1]))
    
    def iterate_keyvalue(self):
        self.__control_exception()
        
        for item in self.__data['return']:
            yield (str(item[0]), item[1])
    
    def iterate_object(self, type):
        self.__control_exception()
        
        for item in self.__data['return']:
            if type is None:
                yield self.__factory.get_instance(item[0], item[1])
            else:
                yield self.__factory.get_instance(type, item)
