import gettext
import sys

from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.model import Project, Solution
from umlfri2.qtgui.base.qtruler import QTRuler
from umlfri2.qtgui import UmlFriMainWindow

app = QApplication(sys.argv)

gettext.install('umlfri2')


def create_example_project():
    ruler = QTRuler()
    project = Project(Application().addons.get_addon('urn:umlfri.org:metamodel:infjavauml').metamodel)
    
    package_type = project.metamodel.get_element_type('package')
    diagram_type = project.metamodel.get_diagram_type('class_diagram')
    
    pkg1 = project.create_child_element(package_type)
    
    pkg1.create_child_diagram(diagram_type)
    
    return project

Application().use_ruler(QTRuler())

project = create_example_project()
Application().solution = Solution(project)

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
