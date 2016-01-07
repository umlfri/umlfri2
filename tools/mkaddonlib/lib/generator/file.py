from .filelistitem import FileListItem


class File(FileListItem):
    def __init__(self, input_file, output_file):
        super().__init__(input_file, output_file, None)
    
    def generate(self, input_file, root):
        with open(input_file, 'rb') as f:
            return f.read()
