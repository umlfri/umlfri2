from .filelistitem import FileListItem


class Generator(FileListItem):
    def generate(self, input_file, root):
        locals = {}
        globals = {}
        with open(input_file) as py_file:
            exec(py_file.read(), globals, locals)
        return locals['generate'](root)
