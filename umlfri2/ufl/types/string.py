from .type import UflType


class UflStringType(UflType):
    def __init__(self, possibilities=None, default=None, template=None, multiline=False):
        self.__default = default or ""
        if possibilities:
            self.__possibilities = tuple(possibilities)
        else:
            self.__possibilities = None
        self.__multiline = multiline
        self.__template = template
    
    @property
    def default(self):
        return self.__default
    
    @property
    def possibilities(self):
        return self.__possibilities
    
    @property
    def multiline(self):
        return self.__multiline
    
    @property
    def template(self):
        return self.__template
    
    def build_default(self, generator):
        if generator is not None and self.__template is not None:
            return generator.get_text(self.__template)
        return ''
    
    def parse(self, value):
        return value
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        return isinstance(value, str)
    
    def is_default_value(self, value):
        return self.__default == value
    
    def __str__(self):
        return 'String'
