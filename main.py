import sys
from PySide.QtGui import QApplication
from umlfri2.components.common import *
from umlfri2.components.expressions import ConstantExpression
from umlfri2.components.expressions.python import PythonExpression
from umlfri2.components.text import *
from umlfri2.components.visual import *
from umlfri2.components.visual.align import HorizontalAlignment
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget
from umlfri2.types.color import Color

app = QApplication(sys.argv)

widget = CanvasWidget()

visual = \
Shadow((
    Rectangle(
        (
            VBox((
                Padding(
                    (
                        Align(
                            (
                                TextBox((), text = PythonExpression(lambda self: self["name"])),
                            ),
                            horizontal=ConstantExpression(HorizontalAlignment.center)
                        ),
                    ),
                    padding=ConstantExpression(5)
                ),
                Line(),
                Table((
                    ForEach(
                        (
                            TableRow(
                                (
                                    TextBox((
                                        Text(text = PythonExpression(lambda self, visibility, name: visibility)),
                                        Text(text = ConstantExpression(" ")),
                                    )),
                                    TextBox((
                                        Text(text = PythonExpression(lambda self, visibility, name: name)),
                                        Text(text = ConstantExpression("()")),
                                    )),
                                )
                            ),
                        ),
                        src=PythonExpression(lambda self: self["items"])
                    ),
                )),
            )),
        ),
        fill=ConstantExpression(Color.get_color("yellow")),
        border=ConstantExpression(Color.get_color("black"))
    ),
))

widget.show_object(visual, {
    "name": "Hello world",
    "items": [
        {"name": "a", "visibility": "+"},
    ]
}, (0, 0), (200, 200))

widget.show_object(visual, {
    "name": "Hello world",
    "items": [
        {"name": "a", "visibility": "+"},
        {"name": "b", "visibility": "-"},
        {"name": "c", "visibility": "#"},
        {"name": "d", "visibility": ""},
    ]
}, (100, 100))

widget.show()

sys.exit(app.exec_())
