from __future__ import annotations

import re
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Pattern


class Version:
    __RE_VERSION: Pattern[str] = re.compile(r'^(?P<version>[0-9]+(\.[0-9]+)*)(-(?P<suffix>(alpha|beta|pre|rc|p))(?P<sufnum>[0-9]+))?$')
    
    def __init__(self, value: str) -> None:
        parsed = self.__RE_VERSION.search(value)
        
        if parsed is None:
            raise Exception("Invalid version number {0}".format(value))
        else:
            ver = tuple(int(i) for i in parsed.group('version').split('.'))
            ver = (ver + (0, 0, 0))[:3]
            
            self.__version: Tuple[int, int, int] = ver  # type: ignore[assignment]
            
            if parsed.group('suffix') is None:
                self.__suffix: Optional[Tuple[str, int]] = None
            else:
                self.__suffix = (parsed.group('suffix'), int(parsed.group('sufnum')))
    
    @property
    def major(self) -> int:
        return self.__version[0]
    
    @property
    def minor(self) -> int:
        return self.__version[1]
    
    @property
    def build(self) -> int:
        return self.__version[2]
    
    @property
    def version(self) -> Tuple[int, int, int]:
        return self.__version
    
    @property
    def suffix(self) -> Optional[Tuple[str, int]]:
        return self.__suffix
    
    @property
    def major_minor_string(self) -> str:
        return "{0}.{1}".format(self.__version[0], self.__version[1])
    
    def is_compatible_with(self, current: Version) -> bool:
        return self.__version[0] == current.__version[0] and self <= current
    
    def __get_comparable(self) -> Tuple[Tuple[int, int, int], Tuple[str, ...]]:
        return self.__version, self.__suffix or ('full', )
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() < other.__get_comparable()
    
    def __le__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() <= other.__get_comparable()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() == other.__get_comparable()
    
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() != other.__get_comparable()
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() > other.__get_comparable()
    
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() >= other.__get_comparable()
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __str__(self) -> str:
        ver = '.'.join(str(part) for part in self.__version)
        if self.__suffix:
            ver += '-{0}{1}'.format(*self.__suffix)
        
        return ver
    
    def __repr__(self) -> str:
        return '<Version {0}>'.format(self)
