from umlfri2.types.enums import ALL_ENUMS

from .any import UflAnyType
from .bool import UflBoolType
from .color import UflColorType
from .decimal import UflDecimalType
from .font import UflFontType
from .image import UflImageType
from .integer import UflIntegerType
from .iterable import UflIterableType
from .list import UflListType
from .nullable import UflNullableType
from .number import UflNumberType
from .object import UflObjectType
from .proportion import UflProportionType
from .string import UflStringType
from .stringenum import UflStringEnumType
from .stringflags import UflStringFlagsType
from .typedenum import UflTypedEnumType


class UflTypeParser:
    def __init__(self, abstract=False):
        self.__abstract = abstract
    
    def has_possibilities(self, type_name):
        return type_name.rstrip('[]?') in ('enum', 'flags', 'str')
    
    def has_template(self, type_name):
        return type_name.rstrip('[]?') == 'str'
    
    def has_attributes(self, type_name):
        return type_name.rstrip('[]?') == 'object'
    
    def parse_default_value(self, type_name, default):
        if default is None:
            return
        
        type_name = type_name.rstrip('[]?')

        if type_name == 'bool':
            return UflBoolType().parse(default)
        elif type_name == 'color':
            return UflColorType().parse(default)
        elif type_name == 'decimal':
            return UflDecimalType().parse(default)
        elif type_name == 'font':
            return UflFontType().parse(default)
        elif type_name == 'image':
            return UflImageType().parse(default)
        elif type_name == 'int':
            return UflIntegerType().parse(default)
        elif type_name == 'proportion':
            return UflProportionType().parse(default)
        
        return default
    
    def parse(self, type_name):
        if type_name == 'any' and self.__abstract:
            return UflAnyType()
        elif type_name == 'bool':
            return UflBoolType()
        elif type_name == 'color':
            return UflColorType()
        elif type_name == 'decimal':
            return UflDecimalType()
        elif type_name == 'font':
            return UflFontType()
        elif type_name == 'image':
            return UflImageType()
        elif type_name == 'int':
            return UflIntegerType()
        elif type_name == 'number' and self.__abstract:
            return UflNumberType()
        elif type_name == 'proportion':
            return UflProportionType()
        elif type_name == 'str':
            return UflStringType()
        elif type_name == 'text':
            return UflStringType(multiline=True)
        elif type_name in ALL_ENUMS:
            return UflTypedEnumType(ALL_ENUMS[type_name])
        
        ret = self.__apply_list(type_name, self.parse)
        if ret is not None:
            return ret
        
        raise Exception("Unknown type {0}".format(type_name))
    
    def parse_with_default(self, type_name, default):
        if self.__abstract:
            raise Exception("Abstract type {0} cannot have a default value ({1})".format(type_name, default))
        
        if type_name == 'bool':
            return UflBoolType(default=default)
        elif type_name == 'color':
            return UflColorType(default=default)
        elif type_name == 'decimal':
            return UflDecimalType(default=default)
        elif type_name == 'font':
            return UflFontType(default=default)
        elif type_name == 'image':
            return UflImageType(default=default)
        elif type_name == 'int':
            return UflIntegerType(default=default)
        elif type_name == 'proportion':
            return UflProportionType(default=default)
        elif type_name == 'str':
            return UflStringType(default=default)
        elif type_name == 'text':
            return UflStringType(default=default, multiline=True)
        elif type_name in ALL_ENUMS:
            return UflTypedEnumType(ALL_ENUMS[type_name], default=default)
        
        ret = self.__apply_list(type_name, self.parse_with_default, default=default)
        if ret is not None:
            return ret
        
        raise Exception("Unknown type with default value: {0}".format(type_name))
    
    def parse_with_template(self, type_name, template):
        if self.__abstract:
            raise Exception("Abstract type {0} cannot have a template".format(type_name))
        
        if type_name == 'str':
            return UflStringType(template=template)
        
        ret = self.__apply_list(type_name, self.parse_with_template, template=template)
        if ret is not None:
            return ret
        
        raise Exception("Unknown type with template: {0}".format(type_name))
    
    def parse_with_possibilities(self, type_name, possibilities):
        if self.__abstract:
            raise Exception("Abstract type {0} cannot have possibilities".format(type_name))
        
        if type_name == 'enum':
            return UflStringEnumType(possibilities)
        elif type_name == 'flags':
            return UflStringFlagsType(possibilities)
        elif type_name == 'str':
            return UflStringType(possibilities)
        
        ret = self.__apply_list(type_name, self.parse_with_possibilities, possibilities=possibilities)
        if ret is not None:
            return ret
        
        raise Exception("Unknown type with possibilities: {0}".format(type_name))
    
    def parse_with_possibilities_and_default(self, type_name, possibilities, default):
        if self.__abstract:
            raise Exception("Abstract type {0} cannot have possibilities".format(type_name))
        
        if type_name == 'enum':
            return UflStringEnumType(possibilities, default=default)
        elif type_name == 'flags':
            return UflStringFlagsType(possibilities, default=default)
        elif type_name == 'str':
            return UflStringType(possibilities, default=default)
        
        ret = self.__apply_list(type_name, self.parse_with_possibilities_and_default, possibilities=possibilities, default=default)
        if ret is not None:
            return ret
        
        raise Exception("Unknown type with possibilities: {0}".format(type_name))
    
    def parse_with_attributes(self, type_name, attributes):
        if self.__abstract:
            raise Exception("Abstract type {0} cannot have attributes".format(type_name))
        
        if type_name == 'object':
            return UflObjectType(attributes)
        
        ret = self.__apply_list(type_name, self.parse_with_attributes, attributes=attributes)
        if ret is not None:
            return ret
        
        raise Exception("Unknown type with attributes: {0}".format(type_name))
    
    def __apply_list(self, type_name, type_parser_method, **kwargs):
        if type_name.endswith('[]'):
            if self.__abstract:
                return UflIterableType(type_parser_method(type_name[:-2], **kwargs))
            else:
                return UflListType(type_parser_method(type_name[:-2], **kwargs))
        
        if type_name.endswith('?'):
            return UflNullableType(type_parser_method(type_name[:-1], **kwargs))
        
        return None
