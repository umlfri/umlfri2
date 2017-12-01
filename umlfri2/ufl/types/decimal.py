from .number import UflNumberType


class UflDecimalType(UflNumberType):
    _PYTHON_TYPE = float
    
    def __str__(self):
        return "Decimal"
