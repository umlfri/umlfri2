import sys

from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.model import Project, Solution
from umlfri2.qtgui.base.qtruler import QTRuler
from umlfri2.qtgui import UmlFriMainWindow
from umlfri2.types.geometry import Point, Size
from umlfri2.ufl.dialog import UflDialog, UflDialogSelectWidget, UflDialogComboWidget, UflDialogChildWidget

app = QApplication(sys.argv)


def print_dialog_tab(tab, indent=0):
    for name, widget in tab.widgets:
        print("    "*indent, name, widget.__class__.__name__)
        if isinstance(widget, (UflDialogSelectWidget, UflDialogComboWidget)):
            for possibility in widget.possibilities:
                print("    "*(indent + 1), possibility)
        elif isinstance(widget, UflDialogChildWidget):
            print_dialog(widget.dialog, indent + 1)


def print_dialog(dialog, indent=0):
    print("    "*indent, "Dialog")
    lonely_tab = dialog.get_lonely_tab()
    if lonely_tab is None:
        for tab in dialog.tabs:
            print("    "*(indent + 1), "Tab", tab.name, tab.__class__.__name__)
            print_dialog_tab(tab, indent + 2)
    else:
        print_dialog_tab(lonely_tab, indent + 1)


def create_example_project():
    ruler = QTRuler()
    project = Project(Application().addons.get_addon('urn:umlfri.org:metamodel:infjavauml').metamodel)
    
    element_type = project.metamodel.get_element_type('class')
    package_type = project.metamodel.get_element_type('package')
    diagram_type = project.metamodel.get_diagram_type('class_diagram')
    connection_type = project.metamodel.get_connection_type('association')
    
    pkg1 = project.create_child_element(package_type)
    
    diagram = pkg1.create_child_diagram(diagram_type)
    diagram2 = pkg1.create_child_diagram(diagram_type)
    
    diagram2_ufl = diagram2.data.make_mutable()
    diagram2_ufl.set_value("name", "Test diagram")
    diagram2.data.apply_patch(diagram2_ufl.make_patch())
    
    obj1 = pkg1.create_child_element(element_type)
    obj2 = pkg1.create_child_element(element_type)
    
    pkg1.create_child_element(package_type)
    
    assoc = obj1.connect_with(connection_type, obj2)
    
    obj1_ufl = obj1.data.make_mutable()
    obj1_ufl.get_value("attributes").append()
    obj1_ufl.get_value("attributes").append()
    obj1_ufl.get_value("attributes").get_item(1).set_value("type", "int")
    obj1_ufl.get_value("operations").append()
    obj1_ufl.get_value("operations").append()
    obj1.data.apply_patch(obj1_ufl.make_patch())
    
    print_dialog(UflDialog(obj1.data.type))
    
    vis1 = diagram.show(obj1)
    vis1.move(ruler, Point(30, 30))
    vis1.resize(ruler, Size(200, 200))
    vis2 = diagram.show(obj2)
    vis2.move(ruler, Point(300, 100))
    vis2.resize(ruler, Size(100, 100))
    
    vispkg1 = diagram.show(pkg1)
    vispkg1.move(ruler, Point(500, 50))
    vispkg1.resize(ruler, Size(200, 200))
    
    diagram.show(assoc)
    
    diagram2.show(pkg1)
    
    return project

Application().use_ruler(QTRuler())

project = create_example_project()
Application().solution = Solution(project)

for element in project.children:
    for diagram in element.diagrams:
        Application().tabs.select_tab(diagram)

window = UmlFriMainWindow()
window.showMaximized()

sys.exit(app.exec_())
