import sys

import appdirs
import lxml.etree
import pyparsing
from PyQt5 import Qt

from .updates import UmlFriUpdates
from umlfri2.types.version import Version


class AboutUmlFri:
    name = "UML .FRI"
    version = Version("2.0")
    
    is_debug_version = __debug__
    
    def __init__(self, application):
        self.__updates = UmlFriUpdates(self, application)

    @property
    def urls(self):
        yield 'http://www.umlfri.org/'
        yield 'https://github.com/umlfri/'
    
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
        yield 'Pyparsing', pyparsing.__version__
    
    @property
    def version_1_contributions(self):
        yield 'Ľubomír Sadloň', (2005, 2008)
        yield 'Ján Janech', (2005, 2015)
        yield 'Pavol Kovalík', (2005, 2007)
        yield 'Marek Dovjak', (2005, 2007)
        yield 'Miroslav Špigura', (2005, 2007)
        yield 'Martina Iskerková', (2006, 2008)
        yield 'Tomáš Bača', (2007, 2011)
        yield 'Milan Juríček', (2007, 2009)
        yield 'Pavol Odlevák', (2007, 2009)
        yield 'Slavomír Kavecký', (2008, 2010)
        yield 'Michal Kováčik', (2008, 2010)
        yield 'Martin Kubinčánek', (2008, 2011)
        yield 'Peter Pajta', (2008, 2010)
        yield 'Katarina Staníková', (2008, 2010)
        yield 'Peter Turza', (2008, 2010)
        yield 'Miloš Korenčiak', (2009, 2010)
        yield 'Tomáš Chabada', (2009, 2010)
        yield 'Marián Kubinčánek', (2009, 2010)
        yield 'Igor Barták', (2010, 2011)
        yield 'Jozef Harabin', (2010, 2012)
        yield 'Matej Jančura', (2011, 2015)
        yield 'Matej Melko', (2011, 2012)
        yield 'Erik Šandor', (2012, 2014)
        yield 'Michal Belás', (2012, 2014)
        yield 'Martin Lokaj', (2012, 2014)
        yield 'Jozef Paľa', (2012, 2015)
        yield 'Miroslav Louma', (2013, 2015)
        yield 'Vincent Jurčišin-Kukľa', (2014, 2016)
    
    @property
    def updates(self):
        return self.__updates
