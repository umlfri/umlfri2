from umlfri2.types.enums import ALL_ENUMS

from .generic import UflAnyType
from .complex import UflColorType
from .basic import UflBoolType, UflDecimalType, UflIntegerType, UflNumberType, UflStringType
from .complex import UflFontType, UflImageType, UflProportionType
from .structured import UflIterableType, UflListType, UflNullableType, UflObjectType
from .enum import UflStringEnumType, UflStringFlagsType, UflTypedEnumType


class UflTypeParserForName:
    __WITH_POSSIBILITIES = {'enum', 'flags', 'str'}
    __WITH_TEMPLATE = {'str'}
    __WITH_ATTRIBUTES = {'object'}
    __WITH_DEFAULT_VALUE = {'bool', 'color', 'decimal', 'font', 'image',
                            'int', 'proportion', 'str', 'text', 'enum',
                            'flags'} | ALL_ENUMS.keys()
    
    def __init__(self, abstract, inner_type, outer_type):
        self.__abstract = abstract
        self.__inner_type = inner_type
        self.__outer_type = outer_type
        self.__default_value = None
        self.__possibilities = None
        self.__attributes = None
        self.__template = None
    
    @property
    def can_have_possibilities(self):
        return self.__inner_type in self.__WITH_POSSIBILITIES
    
    @property
    def can_have_template(self):
        return self.__inner_type in self.__WITH_TEMPLATE
    
    @property
    def can_have_attributes(self):
        return self.__inner_type in self.__WITH_ATTRIBUTES
    
    def set_default_value(self, value):
        if value is None:
            self.__default_value = None
            return
        
        if self.__template is not None:
            raise Exception("Cannot have both value and template specified")
        
        if self.__inner_type not in self.__WITH_DEFAULT_VALUE:
            raise Exception('Cannot have default for a type {0}'.format(self.__inner_type))
        
        self.__default_value = value
    
    def set_default_value_as_string(self, value):
        if value is None:
            self.__default_value = None
            return
        
        if self.__template is not None:
            raise Exception("Cannot have both value and template specified")
        
        if value is not None and self.__inner_type not in self.__WITH_DEFAULT_VALUE:
            raise Exception('Cannot have default for a type {0}'.format(self.__inner_type))
        
        if self.__inner_type == 'bool':
            self.__default_value = UflBoolType().parse(value)
        elif self.__inner_type == 'color':
            self.__default_value = UflColorType().parse(value)
        elif self.__inner_type == 'decimal':
            self.__default_value = UflDecimalType().parse(value)
        elif self.__inner_type == 'font':
            self.__default_value = UflFontType().parse(value)
        elif self.__inner_type == 'image':
            self.__default_value = UflImageType().parse(value)
        elif self.__inner_type == 'int':
            self.__default_value = UflIntegerType().parse(value)
        elif self.__inner_type == 'proportion':
            self.__default_value = UflProportionType().parse(value)
        else:
            self.__default_value = value
    
    def set_possibilities(self, possibilities):
        if not self.can_have_possibilities:
            raise Exception('{0} cannot have possibilities specified'.format(self.__inner_type))
        
        self.__possibilities = tuple(possibilities)
    
    def set_attributes(self, attributes):
        if not self.can_have_attributes:
            raise Exception('{0} cannot have attributes specified'.format(self.__inner_type))
        
        self.__attributes = tuple(attributes)
    
    def set_template(self, template):
        if self.__default_value is not None:
            raise Exception("Cannot have both value and template specified")
        
        if not self.can_have_template:
            raise Exception('{0} cannot have template specified'.format(self.__inner_type))
        
        self.__template = template
    
    def __parse_inner(self):
        if self.__inner_type == 'any' and self.__abstract:
            return UflAnyType()
        elif self.__inner_type == 'bool':
            return UflBoolType(default=self.__default_value)
        elif self.__inner_type == 'color':
            return UflColorType(default=self.__default_value)
        elif self.__inner_type == 'decimal':
            return UflDecimalType(default=self.__default_value)
        elif self.__inner_type == 'font':
            return UflFontType(default=self.__default_value)
        elif self.__inner_type == 'image':
            return UflImageType(default=self.__default_value)
        elif self.__inner_type == 'int':
            return UflIntegerType(default=self.__default_value)
        elif self.__inner_type == 'number' and self.__abstract:
            return UflNumberType()
        elif self.__inner_type == 'proportion':
            return UflProportionType(default=self.__default_value)
        elif self.__inner_type == 'str':
            return UflStringType(possibilities=self.__possibilities, default=self.__default_value, template=self.__template)
        elif self.__inner_type == 'text':
            return UflStringType(default=self.__default_value, multiline=True)
        elif self.__inner_type == 'enum':
            return UflStringEnumType(possibilities=self.__possibilities, default=self.__default_value)
        elif self.__inner_type == 'flags':
            return UflStringFlagsType(possibilities=self.__possibilities, default=self.__default_value)
        elif self.__inner_type == 'object':
            return UflObjectType(self.__attributes)
        elif self.__inner_type in ALL_ENUMS:
            return UflTypedEnumType(ALL_ENUMS[self.__inner_type], default=self.__default_value)
    
    def __parse_outer(self, inner_type):
        if self.__outer_type == '?':
            return UflNullableType(inner_type)
        elif self.__outer_type == '[]':
            if self.__abstract:
                return UflIterableType(inner_type)
            else:
                return UflListType(inner_type)
        elif self.__outer_type is None:
            return inner_type
    
    def finish(self):
        return self.__parse_outer(self.__parse_inner())


class UflTypeParser:
    def __init__(self, abstract=False):
        self.__abstract = abstract
    
    def parse(self, type_name):
        if type_name.endswith('?'):
            return UflTypeParserForName(self.__abstract, type_name[:-1], '?')
        elif type_name.endswith('[]'):
            return UflTypeParserForName(self.__abstract, type_name[:-2], '[]')
        else:
            return UflTypeParserForName(self.__abstract, type_name, None)
