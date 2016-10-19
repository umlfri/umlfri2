from umlfri2.ufl.types import UflObjectType, UflListType, UflColorType, UflFontType


class UflObjectApiHelper:
    def __init__(self, ufl_object):
        self.__ufl_object = ufl_object
    
    def __iter__(self):
        def object_recursion(path, type, obj):
            for attribute in type.attributes:
                attribute_type = attribute.type
                attribute_name = attribute.name
                attribute_value = obj.get_value(attribute_name)
                if path is None:
                    attribute_path = attribute_name
                else:
                    attribute_path = "{0}/{1}".format(path, attribute_name)
                
                if isinstance(attribute_type, UflObjectType):
                    yield from object_recursion(attribute_path, attribute_type, attribute_value)
                elif isinstance(attribute_type, UflListType):
                    yield from list_recursion(attribute_path, attribute_type, attribute_value)
                else:
                    yield attribute_path, self.__convert_get(attribute_type, attribute_value)
        
        def list_recursion(path, type, list):
            item_type = type.item_type
            for no, item_value in enumerate(list):
                if path is None:
                    item_path = str(no)
                else:
                    item_path = "{0}/{1}".format(path, no)
                if isinstance(item_type, UflObjectType):
                    yield from object_recursion(item_path, item_type, item_value)
                elif isinstance(item_type, UflListType):
                    yield from list_recursion(item_path, item_type, item_value)
                else:
                    yield item_path, self.__convert_get(item_type, item_value)
        
        return object_recursion(None, self.__ufl_object.type, self.__ufl_object)
    
    def __convert_get(self, type, value):
        if isinstance(type, (UflObjectType, UflListType)):
            raise Exception("Invalid type - can return only primitive types")
        
        if isinstance(type, (UflColorType, UflFontType)):
            return str(value)
        
        return value
    
    def __getitem__(self, item):
        path = item.split('/')
        obj = self.__ufl_object
        type = self.__ufl_object.type
        
        for part in path:
            if isinstance(type, UflObjectType):
                type = type.get_attribute(part).type
                obj = obj.get_value(part)
            elif isinstance(type, UflListType):
                type = type.item_type
                obj = obj.get_item(int(part))
            else:
                raise Exception
        
        return self.__convert_get(type, obj)
