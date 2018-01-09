import os

from .filechannel import FileChannel

try:
    from msvcrt import get_osfhandle
except ImportError:
    def get_osfhandle(fd):
        return fd


class PipeChannel(FileChannel):
    def __init__(self):
        read_my, write_child = os.pipe()
        read_child, write_my = os.pipe()
        
        os.set_inheritable(read_child, True)
        os.set_inheritable(write_child, True)
        
        super().__init__(os.fdopen(read_my, 'rb'), os.fdopen(write_my, 'wb'))
        
        self.__read_child = read_child
        self.__write_child = write_child
    
    @property
    def child_reader_handle(self):
        return get_osfhandle(self.__read_child)
    
    @property
    def child_writer_handle(self):
        return get_osfhandle(self.__write_child)
    
    def close_child_descriptors(self):
        os.close(self.__read_child)
        os.close(self.__write_child)
