import sys
from PySide.QtGui import QApplication
import lxml.etree
from umlfri2.metamodel.loader import ElementTypeLoader, AddonInfoLoader
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget

app = QApplication(sys.argv)

widget = CanvasWidget()

addon = AddonInfoLoader(lxml.etree.parse(open('addons/infjavauml/addon.xml')).getroot()).load()

type = ElementTypeLoader(addon, lxml.etree.parse(open('addons/infjavauml/metamodel/classDiagram/class.xml')).getroot()).load()
type.compile()

obj1 = type.ufl_type.build_default()
obj2 = type.ufl_type.build_default()

obj1.get_value("attributes").append()
obj1.get_value("attributes").append()
obj1.get_value("attributes").get_item(0).set_value("name", "attr")
obj1.get_value("attributes").get_item(1).set_value("name", "attr2")
obj1.get_value("attributes").get_item(1).set_value("type", "int")

obj1.set_value("name", "Class1")
obj2.set_value("name", "Class2")

widget.show_object(type, obj1, (30, 30))

widget.show_object(type, obj2, (10, 10))

widget.show()

sys.exit(app.exec_())
