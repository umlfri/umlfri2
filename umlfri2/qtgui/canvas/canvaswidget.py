from PySide.QtGui import QWidget, QPainter
from umlfri2.components.base.context import Context
from umlfri2.qtgui.canvas.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.canvas.qtruler import QTRuler


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__objects = []
        self.__ruler = QTRuler()
    
    # TODO: object should contain type witch should contain component
    def show_object(self, type, obj, position=(0, 0), size=None):
        obj = type.create_visual_object(Context(obj), self.__ruler)
        obj.move(position)
        obj.resize(size)
        self.__objects.append(obj)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        canvas = QTPainterCanvas(painter)
        for obj in self.__objects:
            obj.draw(canvas)
        painter.end()
