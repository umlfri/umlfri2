from .type import UflType


class UflProportionType(UflType):
    def __init__(self, allow_over_one=False, default=None):
        self.__default = default
        self.__allow_over_one = allow_over_one
    
    @property
    def allow_over_one(self):
        return self.__allow_over_one
    
    @property
    def default(self):
        return self.__default
    
    def build_default(self):
        return self.__default or Colors.black
    
    def parse(self, value):
        if ':' in value:
            antecedent, consequent = value.split(':', 1)
            return int(antecedent) / (int(consequent) + int(antecedent))
        elif '/' in value:
            numerator, denominator = value.split('/', 1)
            return int(numerator) / int(denominator)
        elif value.endswith('%'):
            return float(value[:-1]) / 100
        else:
            return float(value)
    
    @property
    def is_immutable(self):
        return True
    
    def is_valid_value(self, value):
        if not isinstance(value, float):
            return False
        
        if value < 0:
            return False
        
        if not self.allow_over_one and value > 1:
            return False
        
        return True
    
    def __str__(self):
        return 'Proportion'
