from .filelistitem import FileListItem
from .file import File

import glob
import os
import os.path


class Directory(FileListItem):
    def __init__(self, input_file, output_file, glob):
        super().__init__(input_file, output_file, None)
        
        self.__glob = glob
    
    def sub_items(self, input_file, output_file):
        for item in glob.glob(os.path.join(input_file, self.__glob)):
            yield File(item, os.path.join(output_file, os.path.basename(item)))
        
        for item in os.listdir(input_file):
            itemPath = os.path.join(input_file, item)
            if os.path.isdir(itemPath) and not item.startswith('.'):
                yield Directory(itemPath, os.path.join(output_file, item), self.__glob)
