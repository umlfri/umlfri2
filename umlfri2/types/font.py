from __future__ import annotations

from typing import FrozenSet, Iterable, Set

from umlfri2.types.enums import FontStyle


class Font:
    def __init__(self, family: str, size: int, style: Iterable[FontStyle] = ()) -> None:
        self.__family = family
        self.__size = size
        self.__style = frozenset(style)
    
    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def family(self) -> str:
        return self.__family
    
    @property
    def style(self) -> FrozenSet[FontStyle]:
        return self.__style
    
    def change_family(self, new_family: str) -> Font:
        return Font(new_family, self.__size, self.__style)
    
    def change_size(self, new_size: int) -> Font:
        return Font(self.__family, new_size, self.__style)
    
    def change(self, style: FontStyle, value: bool) -> Font:
        new_style = set(self.__style)
        
        if value:
            new_style.add(style)
        elif style in new_style:
            new_style.remove(style)
        return Font(self.__family, self.__size, new_style)
    
    def __str__(self) -> str:
        if self.__style:
            return "{0} {1} {2}".format(self.__family, ' '.join(i.name for i in self.__style), self.__size)
        else:
            return "{0} {1}".format(self.__family, self.__size)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Font):
            return self.__family == other.__family and self.__style == other.__style and self.__size == other.__size
        return NotImplemented
    
    @staticmethod
    def get_font(description: str) -> Font:
        tmp = description.split()
        size = int(tmp.pop(-1))
        
        style = set()
        while tmp[-1] in FontStyle.__members__:
            style.add(FontStyle[tmp.pop(-1)])
        
        family = ' '.join(tmp)
        
        return Font(family, size, style)


class Fonts:
    default = Font('Arial', 10)
    
    @staticmethod
    def exists(name: str) -> bool:
        return isinstance(getattr(Fonts, name, None), Font)
    
    @staticmethod
    def get(name: str) -> Font:
        return getattr(Fonts, name)
