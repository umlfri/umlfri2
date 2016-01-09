import os
import os.path
import sys

from umlfri2.plugin.starters import BaseProgramStarter

ADDON_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class PythonStarter(BaseProgramStarter):
    program = (sys.executable, os.path.join(ADDON_ROOT_PATH, 'starter', 'python_runner.py'))
    environment = {
        'LIB': os.path.join(ADDON_ROOT_PATH, 'library'),
        'PATH': '{path}'
    }
