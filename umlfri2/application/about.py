import sys

import appdirs
import lxml.etree
from PyQt5 import Qt

from umlfri2.types.version import Version


class AboutUmlFri:
    name = "UML .FRI"
    version = Version("2.0")
    
    @property
    def author(self):
        yield "Ján Janech", (2015, 2017)
    
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
    
    @property
    def version_1_contributions(self):
        yield 'Lubomir Sadlon', (2005, 2008)
        yield 'Jan Janech', (2005, 2015)
        yield 'Pavol Kovalik', (2005, 2007)
        yield 'Marek Dovjak', (2005, 2007)
        yield 'Miroslav Spigura', (2005, 2007)
        yield 'Martina Iskerkova', (2006, 2008)
        yield 'Tomas Baca', (2007, 2011)
        yield 'Milan Juricek', (2007, 2009)
        yield 'Pavol Odlevak', (2007, 2009)
        yield 'Slavomir Kavecky', (2008, 2010)
        yield 'Michal Kovacik', (2008, 2010)
        yield 'Martin Kubincanek', (2008, 2011)
        yield 'Peter Pajta', (2008, 2010)
        yield 'Katarina Stanikova', (2008, 2010)
        yield 'Peter Turza', (2008, 2010)
        yield 'Milos Korenciak', (2009, 2010)
        yield 'Tomas Chabada', (2009, 2010)
        yield 'Marian Kubincanek', (2009, 2010)
        yield 'Igor Bartak', (2010, 2011)
        yield 'Jozef Harabin', (2010, 2012)
        yield 'Matej Jancura', (2011, 2012)
        yield 'Matej Melko', (2011, 2012)
