from __future__ import annotations

import math


class Proportion:
    def __init__(self, antecedent: int, consequent: int) -> None:
        gcd = math.gcd(antecedent, consequent)
        self.__antecedent = antecedent // gcd
        self.__consequent = consequent // gcd
        self.__value = self.__antecedent / (self.__antecedent + self.__consequent)
    
    @property
    def antecedent(self) -> int:
        return self.__antecedent
    
    @property
    def consequent(self) -> int:
        return self.__consequent
    
    @property
    def ratio(self) -> str:
        return "{0}:{1}".format(self.__antecedent, self.__consequent)
    
    @property
    def fraction(self) -> str:
        return "{0}/{1}".format(self.__antecedent, self.__antecedent + self.__consequent)
    
    @property
    def percentage(self) -> str:
        return "{0:.2g}%".format(round(self.__value, 2))
    
    @property
    def value(self) -> float:
        return self.__value
    
    @staticmethod
    def from_ratio(antecedent: int, consequent: int) -> Proportion:
        if antecedent < 0 or consequent < 0:
            raise Exception("Invalid proportion")
        if antecedent == 0 and consequent == 0:
            raise Exception("Invalid proportion")
        
        return Proportion(antecedent, consequent)
    
    @staticmethod
    def from_fraction(numerator: int, denominator: int) -> Proportion:
        if numerator > denominator:
            raise Exception("Invalid proportion")
        
        if numerator < 0 or denominator < 0:
            raise Exception("Invalid proportion")
        
        if denominator == 0:
            raise Exception("Invalid proportion")
        
        return Proportion(numerator, denominator - numerator)
    
    @staticmethod
    def from_percentage(percentage: float) -> Proportion:
        return Proportion.from_value(percentage / 100)
    
    @staticmethod
    def from_value(value: float) -> Proportion:
        if value < 0 or value > 1:
            raise Exception("Invalid proportion")
        
        antecedent = int(round(value, 4)*10000)
        
        return Proportion(antecedent, 10000 - antecedent)
    
    @staticmethod
    def from_string(proportion: str) -> Proportion:
        if ':' in proportion:
            antecedent, consequent = proportion.split(':', 1)
            return Proportion.from_ratio(int(antecedent), int(consequent))
        elif '/' in proportion:
            numerator, denominator = proportion.split('/', 1)
            return Proportion.from_fraction(int(numerator), int(denominator))
        elif proportion.endswith('%'):
            return Proportion.from_percentage(float(proportion[:-1]))
        else:
            return Proportion.from_value(float(proportion))
    
    def __str__(self) -> str:
        return self.ratio
    
    def __repr__(self) -> str:
        return "<Proportion {0}>".format(self.ratio)


WHOLE_PROPORTION = Proportion(1, 0)
EMPTY_PROPORTION = Proportion(0, 1)
