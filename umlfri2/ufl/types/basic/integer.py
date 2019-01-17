from .number import UflNumberType


class UflIntegerType(UflNumberType):
    _PYTHON_TYPE = int
    
    def __str__(self):
        return "Integer"
