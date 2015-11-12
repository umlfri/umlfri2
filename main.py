import sys

from PySide.QtGui import QApplication

from umlfri2.application import Application
from umlfri2.model import Project, Solution
from umlfri2.qtgui.canvas import QTRuler
from umlfri2.qtgui import UmlFriMainWindow
from umlfri2.types.geometry import Point, Size


app = QApplication(sys.argv)

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
    diagram2.data.set_value("name", "Test diagram")
    
    obj1 = pkg1.create_child_element(element_type)
    obj2 = pkg1.create_child_element(element_type)
    
    pkg1.create_child_element(package_type)
    
    assoc = obj1.connect_with(connection_type, obj2)
    assoc.data.set_value("name", "assoc")
    
    obj1.data.get_value("attributes").append()
    obj1.data.get_value("attributes").append()
    obj1.data.get_value("attributes").get_item(1).set_value("type", "int")
    obj1.data.get_value("operations").append()
    obj1.data.get_value("operations").append()
    
    vis1 = diagram.show(obj1)
    vis1.move(ruler, Point(30, 30))
    vis1.resize(ruler, Size(200, 200))
    vis2 = diagram.show(obj2)
    vis2.move(ruler, Point(300, 100))
    vis2.resize(ruler, Size(100, 100))
    
    vispkg1 = diagram.show(pkg1)
    vispkg1.move(ruler, Point(500, 50))
    vispkg1.resize(ruler, Size(200, 200))
    
    visassoc = diagram.show(assoc)
    visassoc.add_point(ruler, Point(500, 300))
    
    diagram2.show(pkg1)
    
    return project

project = create_example_project()
Application().solution = Solution(project)

for element in project.children:
    for diagram in element.diagrams:
        Application().tabs.open_tab(diagram)

window = UmlFriMainWindow()
window.showMaximized()

def show_tree(node, indent = 0):
    print('    '*indent + node.get_display_name())
    if not isinstance(node, Project):
        for diagram in node.diagrams:
            print('    '*(indent + 1) + '*' + diagram.get_display_name())
    for child in node.children:
        show_tree(child, indent + 1)

show_tree(project)

sys.exit(app.exec_())
