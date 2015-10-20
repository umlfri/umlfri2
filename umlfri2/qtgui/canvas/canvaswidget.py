from PySide.QtGui import QWidget, QPainter
from umlfri2.components.base.context import Context
from umlfri2.qtgui.canvas.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.canvas.qtruler import QTRuler


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__objects = []
        self.__ruler = QTRuler()
    
    def show_object(self, visual):
        self.__objects.append(visual)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        canvas = QTPainterCanvas(painter)
        for visual in self.__objects:
            visual.draw(canvas)
        painter.end()
    
    def get_ruler(self):
        return self.__ruler
