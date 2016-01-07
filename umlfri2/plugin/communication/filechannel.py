import json
import threading

from .channel import Channel


class FileChannel(Channel):
    __encoder = json.JSONEncoder(ensure_ascii=False, check_circular=False, allow_nan=False)
    __decoder = json.JSONDecoder()
    
    def __init__(self, input, output):
        self.__input = input
        self.__output = output
        self.__write_lock = threading.Lock()
        self.__read_lock = threading.Lock()
        
        self.__closed = False
    
    def write(self, data):
        with self.__write_lock:
            if self.__closed:
                raise Exception
            
            for chunk in self.__encoder.iterencode(data):
                self.__output.write(chunk.encode('utf8'))
            
            self.__output.write('\r\n')
            self.__output.flush()
    
    def read(self):
        with self.__read_lock:
            if self.__closed:
                raise Exception
            
            while True:
                ret = self.__input.readline()
                if ret:
                    return self.__decoder.decode(ret.rstrip('\r\n').decode('utf8'))
                else:
                    self.__closed = True
                    return
    
    def close(self):
        self.__input.close()
        self.__output.close()
        self.__closed = True
    
    @property
    def closed(self):
        return self.__closed
