import os
import os.path


class FileListItem:
    def __init__(self, input_file, output_file, root):
        self.__input_file = input_file
        self.__output_file = output_file
        self.__root = root
    
    def create(self, dir):
        sub_items = self.sub_items(self.__input_file, self.__output_file)
        
        if sub_items is not None:
            for sub_item in sub_items:
                sub_item.create(dir)
        else:
            relative_directory = os.path.dirname(self.__output_file)
            relative_filefile = os.path.basename(self.__output_file)
            dir = os.path.abspath(os.path.join(dir, relative_directory))
            
            self.__mkdir(dir)
            
            self.create_file(self.__input_file, os.path.join(dir, relative_filefile), self.__root)
        
    def create_file(self, input_file, output_file, root):
        with open(output_file, 'wb') as f:
            f.write(self.generate(input_file, root))
    
    def sub_items(self, input_file, output_file):
        return None
    
    def generate(self, input_file, root):
        raise Exception
    
    def finish(self):
        pass
    
    def __mkdir(self, dir):
        if not os.path.exists(dir):
            self.__mkdir(os.path.dirname(dir))
            os.mkdir(dir)
