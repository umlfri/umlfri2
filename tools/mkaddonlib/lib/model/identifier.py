import re


class Identifier:
    __reIdentifierSplitter = re.compile('([A-Z][a-z0-9]+)')
    
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__split_identifier = [part.lower() for part in self.__reIdentifierSplitter.split(identifier) if part]
    
    @property
    def default(self):
        return self.__identifier
    
    @property
    def upper_camel_case(self):
        return ''.join(part.capitalize() for part in self.__split_identifier)
    
    @property
    def lower_camel_case(self):
        return self.__split_identifier[0] + ''.join(part.capitalize() for part in self.__split_identifier[1:])
    
    @property
    def lower_underscore_separated(self):
        return '_'.join(self.__split_identifier)
    
    @property
    def upper_underscore_separated(self):
        return '_'.join(self.__split_identifier).upper()
    
    @property
    def lower_dash_separated(self):
        return '-'.join(self.__split_identifier)
    
    @property
    def upper_dash_separated(self):
        return '-'.join(self.__split_identifier).upper()
    
    @property
    def lower_case(self):
        return ''.join(self.__split_identifier)
    
    @property
    def upper_case(self):
        return ''.join(part.upper() for part in self.__split_identifier)
    
    def __add__(self, str):
        return Identifier(self.lower_camel_case + str)
    
    def __radd__(self, str):
        return Identifier(str + self.upper_camel_case)
