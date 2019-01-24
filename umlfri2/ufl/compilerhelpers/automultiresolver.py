from collections import namedtuple

from ..types.structured import UflIterableType, UflListType, UflNullableType
from ..types.enum import UflFlagsType


MultiType = namedtuple('MultiType', ['type', 'is_multi_invoke', 'is_null_invoke'])


def resolve_multi_source(registrar, target_type, src_format, target):
    if isinstance(target_type, (UflIterableType, UflListType, UflFlagsType)):
        var = registrar.register_temp_variable()
        
        src = src_format.format(var)
        
        return "({0} for {1} in ({2}))".format(src, var, target)
    elif isinstance(target_type, UflNullableType):
        var = registrar.register_temp_variable()
    
        src = src_format.format(var)
    
        return "(lambda {0}: None if {0} is None else {1})({2})".format(var, src, target)
    else:
        return src_format.format(target)


def resolve_multi_type(target_type):
    if isinstance(target_type, (UflIterableType, UflListType, UflFlagsType)):
        return MultiType(target_type.item_type, True, False)
    elif isinstance(target_type, UflNullableType):
        return MultiType(target_type.inner_type, False, True)
    else:
        return MultiType(target_type, False, False)
