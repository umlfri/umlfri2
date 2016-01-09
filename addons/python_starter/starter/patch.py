from umlfri2.plugin.starters import STARTER_LIST

from .python_starter import PythonStarter


class Patch:
    def start(self):
        STARTER_LIST['python'] = PythonStarter
    
    def stop(self):
        STARTER_LIST['python'] = PythonStarter
