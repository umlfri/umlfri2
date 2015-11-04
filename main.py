import sys
from PySide.QtGui import QApplication
from umlfri2.addon.loader import AddOnLoader
from umlfri2.model import Diagram, ElementObject
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget
from umlfri2.types.geometry import Point, Size

app = QApplication(sys.argv)

widget = CanvasWidget()
ruler = widget.get_ruler()

addon = AddOnLoader('addons/infjavauml').load()

element_type = addon.metamodel.get_element_type('class')
diagram_type = addon.metamodel.get_diagram_type('class_diagram')
connection_type = addon.metamodel.get_connection_type('association')

diagram = Diagram(diagram_type)

obj1 = ElementObject(element_type)
obj2 = ElementObject(element_type)

assoc = obj1.connect_with(connection_type, obj2)
assoc.data.set_value("name", "assoc")

obj1.data.get_value("attributes").append()
obj1.data.get_value("attributes").append()
obj1.data.get_value("attributes").get_item(0).set_value("name", "attr")
obj1.data.get_value("attributes").get_item(1).set_value("name", "attr2")
obj1.data.get_value("attributes").get_item(1).set_value("type", "int")

obj1.data.set_value("name", "Class1")
obj2.data.set_value("name", "Class2")

print(obj1.get_display_name())
print(obj2.get_display_name())

vis1 = diagram.show(obj1)
vis1.move(ruler, Point(30, 30))
vis1.resize(ruler, Size(200, 200))
vis2 = diagram.show(obj2)
vis2.move(ruler, Point(300, 100))
vis2.resize(ruler, Size(100, 100))

visassoc = diagram.show(assoc)
visassoc.add_point(ruler, Point(500, 300))

widget.show_diagram(diagram)

widget.show()

sys.exit(app.exec_())
