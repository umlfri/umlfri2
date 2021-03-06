from hashlib import sha256
import sys
from enum import Enum
from urllib.request import urlopen


class OnlineAddOnArch(Enum):
    processor_32 = 1
    processor_64 = 2


class OnlineAddOnHash(Enum):
    sha256 = (sha256, )
    
    def __init__(self, fnc):
        self.__fnc = fnc
    
    def compute(self, bytes):
        return self.__fnc(bytes).hexdigest()


class OnlineAddOnLocation:
    def __init__(self, url, hash, hash_type, arch=None, os=None):
        self.__url = url
        self.__hash = hash
        self.__hash_type = hash_type
        self.__arch = arch
        self.__os = os
    
    @property
    def url(self):
        return self.__url
    
    @property
    def is_valid(self):
        if self.__os is not None and not sys.platform.startswith(self.__os):
            return False
        
        if self.__arch == OnlineAddOnArch.processor_32 and sys.maxsize > 2**32:
            return False

        if self.__arch == OnlineAddOnArch.processor_64 and sys.maxsize <= 2**32:
            return False
        
        return True
    
    def download(self):
        data = urlopen(self.__url).read()
        hash = self.__hash_type.compute(data)
        
        if hash != self.__hash:
            raise Exception("Invalid hash")
        
        return data
