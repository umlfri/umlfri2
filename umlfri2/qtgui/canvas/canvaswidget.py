from PySide.QtCore import Qt, QPoint
from PySide.QtGui import QWidget, QPainter, QColor, QFont
from umlfri2.components.base.context import Context
from umlfri2.qtgui.canvas.qtpaintercanvas import QTPainterCanvas


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__objects = []
    
    # TODO: object should contain type witch should contain component
    def show_object(self, component, obj):
        self.__objects.append((component, obj))
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        canvas = QTPainterCanvas(painter)
        for component, obj in self.__objects:
            ctx = Context(obj)
            component.draw(ctx, canvas, (0, 0, None, None))
        painter.end()
