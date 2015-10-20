import sys
from PySide.QtGui import QApplication
import lxml.etree
from umlfri2.metamodel.loader import ElementTypeLoader, AddonInfoLoader
from umlfri2.model.element import ElementObject, ElementVisual
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget

app = QApplication(sys.argv)

widget = CanvasWidget()
ruler = widget.get_ruler()

addon = AddonInfoLoader(lxml.etree.parse(open('addons/infjavauml/addon.xml')).getroot()).load()

type = ElementTypeLoader(addon, lxml.etree.parse(open('addons/infjavauml/metamodel/classDiagram/class.xml')).getroot()).load()
type.compile()

obj1 = ElementObject(type)
obj2 = ElementObject(type)

obj1.data.get_value("attributes").append()
obj1.data.get_value("attributes").append()
obj1.data.get_value("attributes").get_item(0).set_value("name", "attr")
obj1.data.get_value("attributes").get_item(1).set_value("name", "attr2")
obj1.data.get_value("attributes").get_item(1).set_value("type", "int")

obj1.data.set_value("name", "Class1")
obj2.data.set_value("name", "Class2")

print(obj1.get_display_name())
print(obj2.get_display_name())

vis1 = ElementVisual(obj1)
vis2 = ElementVisual(obj2)
vis1.move(ruler, (30, 30))
vis1.resize(ruler, (200, 200))
vis2.move(ruler, (10, 10))

widget.show_object(vis1)
widget.show_object(vis2)

widget.show()

sys.exit(app.exec_())
