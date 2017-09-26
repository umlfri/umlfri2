import re


class Version:
    __RE_VERSION = re.compile(r'^(?P<version>[0-9]+(\.[0-9]+)*)(-(?P<suffix>(alpha|beta|pre|rc|p))(?P<sufnum>[0-9]+))?$')
    
    def __init__(self, value):
        parsed = self.__RE_VERSION.search(value)
        
        if parsed is None:
            raise Exception("Invalid version number {0}".format(value))
        else:
            ver = tuple(int(i) for i in parsed.group('version').split('.'))
            ver = (ver + (0, 0, 0))[:3]
            
            self.__version = ver
            
            if parsed.group('suffix') is None:
                self.__suffix = None
            else:
                self.__suffix = (parsed.group('suffix'), int(parsed.group('sufnum')))
    
    @property
    def version(self):
        return self.__version
    
    @property
    def suffix(self):
        return self.__suffix
    
    @property
    def major_minor_string(self):
        return "{0}.{1}".format(self.__version[0], self.__version[1])
    
    def __get_comparable(self):
        return self.__version, self.__suffix or ('full', )
    
    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() < other.__get_comparable()
    
    def __le__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() <= other.__get_comparable()
    
    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() == other.__get_comparable()
    
    def __ne__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() != other.__get_comparable()
    
    def __gt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() > other.__get_comparable()
    
    def __ge__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        
        return self.__get_comparable() >= other.__get_comparable()
    
    def __hash__(self):
        return hash(str(self))
    
    def __str__(self):
        ver = '.'.join(str(part) for part in self.__version)
        if self.__suffix:
            ver += '-{0}{1}'.format(*self.__suffix)
        
        return ver
    
    def __repr__(self):
        return '<Version {0}>'.format(self)
