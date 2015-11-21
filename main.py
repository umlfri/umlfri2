import gettext
import sys

import lxml.etree
from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.datalayer.loaders.projectloader import ProjectLoader
from umlfri2.model import Solution
from umlfri2.qtgui.base.qtruler import QTRuler
from umlfri2.qtgui import UmlFriMainWindow

app = QApplication(sys.argv)

gettext.install('umlfri2')

Application().use_ruler(QTRuler())

project_loader = ProjectLoader(
    lxml.etree.parse(open('addons/infjavauml/metamodel/templates/example.xml')).getroot(),
    Application().ruler,
    Application().addons
)

Application().solution = Solution(project_loader.load())

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
