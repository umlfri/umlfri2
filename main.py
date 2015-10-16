import sys
from PySide.QtGui import QApplication
from umlfri2.components.common import *
from umlfri2.components.expressions import ConstantExpression, UflExpression
from umlfri2.components.text import *
from umlfri2.components.visual import *
from umlfri2.components.visual.align import HorizontalAlignment
from umlfri2.metamodel import ElementType
from umlfri2.qtgui.canvas.canvaswidget import CanvasWidget
from umlfri2.types.color import Colors
from umlfri2.ufl.types import *

app = QApplication(sys.argv)

widget = CanvasWidget()

test_type = ElementType(
    'test_type',
    UflObjectType({
        'name': UflStringType(),
        'items': UflListType(
            UflObjectType({
                'name': UflStringType(),
                'visibility': UflEnumType(('+', '-', '#'))
            })
        )
    }),
    Text(text=UflExpression('self.name')),
    Shadow((
        Rectangle(
            (
                VBox((
                    Padding(
                        (
                            Align(
                                (
                                    TextBox((), text = UflExpression('self.name')),
                                ),
                                horizontal=ConstantExpression(HorizontalAlignment.center, UflTypedEnumType(HorizontalAlignment))
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
                                            Text(text = UflExpression('visibility')),
                                            Text(text = ConstantExpression(" ")),
                                        )),
                                        TextBox((
                                            Text(text = UflExpression('name')),
                                            Text(text = ConstantExpression("()")),
                                        )),
                                    )
                                ),
                            ),
                            src=UflExpression('self.items')
                        ),
                    )),
                )),
            ),
            fill=ConstantExpression(Colors.yellow),
            border=ConstantExpression(Colors.black)
        ),
    ))
)

test_type.compile()

widget.show_object(test_type, {
    "name": "Hello world",
    "items": [
        {"name": "a", "visibility": "+"},
    ]
}, (0, 0), (200, 200))

widget.show_object(test_type, {
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
