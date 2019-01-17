from umlfri2.ufl.types.structured import UflObjectType, UflListType
from umlfri2.ufl.types.enum import UflFlagsType


def check_any(type, data):
    if isinstance(type, UflObjectType):
        return check_object(type, data)
    elif isinstance(type, UflListType):
        return check_list(type, data)
    elif isinstance(type, UflFlagsType):
        return check_flags(type, data)
    elif type.is_immutable:
        if not isinstance(data, str):
            raise Exception("Value expected")
        return type.parse(data)
    else:
        raise Exception


def check_object(type, data):
    if not data:
        return {}
    
    if not isinstance(data, dict):
        raise Exception("Expecting object")
    
    ret = {}
    for name, value in data.items():
        if not type.contains_attribute(name):
            raise Exception("There is no {0} attribute".format(name))
        ret[name] = check_any(type.get_attribute(name).type, value)
    
    return ret


def check_list(type, data):
    if not data:
        return []

    if not isinstance(data, list):
        raise Exception("Expecting list")
    
    item_type = type.item_type
    ret = []
    for value in data:
        ret.append(check_any(item_type, value))

    return ret


def check_flags(type, data):
    if not data:
        return []

    if not isinstance(data, list) and not all(isinstance(i, str) for i in data):
        raise Exception("Expecting flags")
    
    return data
