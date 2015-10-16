import sys
from PySide.QtGui import QApplication
import lxml.etree
from umlfri2.components.common import *
from umlfri2.components.expressions import ConstantExpression, UflExpression
from umlfri2.components.text import *
from umlfri2.components.visual import *
from umlfri2.components.visual.align import HorizontalAlignment
from umlfri2.metamodel import ElementType
from umlfri2.metamodel.loader import ElementTypeLoader
from umlfri2.metamodel.loader.addoninfoloader import AddonInfoLoader
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget
from umlfri2.types.color import Colors
from umlfri2.ufl.types import *

app = QApplication(sys.argv)

widget = CanvasWidget()

addon = AddonInfoLoader(lxml.etree.parse(open('addons/infjavauml/addon.xml')).getroot()).load()

type = ElementTypeLoader(addon, lxml.etree.parse(open('addons/infjavauml/metamodel/classDiagram/class.xml')).getroot()).load()
type.compile()

obj1 = type.ufl_type.build_default()
obj2 = type.ufl_type.build_default()

obj1["name"] = "Class1"
obj2["name"] = "Class2"

widget.show_object(type, obj1, (30, 30))

widget.show_object(type, obj2, (0, 0))

widget.show()

sys.exit(app.exec_())
