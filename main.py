import gettext
import sys

from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.model import Project, Solution
from umlfri2.qtgui.base.qtruler import QTRuler
from umlfri2.qtgui import UmlFriMainWindow

app = QApplication(sys.argv)

gettext.install('umlfri2')

Application().use_ruler(QTRuler())

project = Project(Application().addons.get_addon('urn:umlfri.org:metamodel:infjavauml').metamodel)
Application().solution = Solution(project)

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
