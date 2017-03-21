import sys

import appdirs
import lxml.etree
from PyQt5 import Qt

from umlfri2.types.version import Version


class AboutUmlFri:
    name = "UML .FRI"
    version = Version("2.0")
    
    author = "© 2015-2017 Ján Janech"
    
    @property
    def description(self):
        return _("Free Python-based DSM CASE tool targeted on computer sciences education")
    
    @property
    def dependency_versions(self):
        yield 'Python', "%s.%s.%s"%sys.version_info[:3]
        yield 'Qt', Qt.QT_VERSION_STR
        yield 'PyQt', Qt.PYQT_VERSION_STR
        yield 'AppDirs', appdirs.__version__
        yield 'lxml', lxml.etree.__version__
