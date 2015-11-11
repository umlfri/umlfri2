import sys

from PySide.QtGui import QApplication

from umlfri2.datalayer.loaders import AddOnLoader
from umlfri2.datalayer.storages import Storage
from umlfri2.model import Project
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget
from umlfri2.types.geometry import Point, Size


app = QApplication(sys.argv)

widget = CanvasWidget()
ruler = widget.get_ruler()

addon = AddOnLoader(Storage.open('addons/infjavauml')).load()

project = Project(addon.metamodel)

element_type = project.metamodel.get_element_type('class')
package_type = project.metamodel.get_element_type('package')
diagram_type = project.metamodel.get_diagram_type('class_diagram')
connection_type = project.metamodel.get_connection_type('association')

pkg1 = project.create_child_element(package_type)

diagram = pkg1.create_child_diagram(diagram_type)

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

widget.show_diagram(diagram)

widget.show()

def show_tree(node, indent = 0):
    print('    '*indent + node.get_display_name())
    if not isinstance(node, Project):
        for diagram in node.diagrams:
            print('    '*(indent + 1) + '*' + diagram.get_display_name())
    for child in node.children:
        show_tree(child, indent + 1)

show_tree(project)

sys.exit(app.exec_())
