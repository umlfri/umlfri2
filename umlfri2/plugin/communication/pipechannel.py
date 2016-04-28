import os

from .filechannel import FileChannel


class PipeChannel(FileChannel):
    def __init__(self):
        if hasattr(os, 'pipe2'):
            read_my, write_child = os.pipe2(0)
            read_child, write_my = os.pipe2(0)
        else:
            read_my, write_child = os.pipe()
            read_child, write_my = os.pipe()
        
        super().__init__(os.fdopen(read_my, 'rb'), os.fdopen(write_my, 'wb'))
        
        self.__read_child = read_child
        self.__write_child = write_child
    
    @property
    def child_reader_descriptor(self):
        return self.__read_child
    
    @property
    def child_writer_descriptor(self):
        return self.__write_child
    
    def close_child_descriptors(self):
        os.close(self.__read_child)
        os.close(self.__write_child)
