from .filelistitem import FileListItem
from .jinjaenv import JINJA_ENV


class Template(FileListItem):
    def __init__(self, input_file, output_file, root, modules):
        super().__init__(input_file, output_file, root)
        self.__modules = modules
    
    def generate(self, input_file, root):
        with open(input_file) as template_file:
            return JINJA_ENV.from_string(template_file.read()).render(root=root, **self.__modules).encode('utf8')
