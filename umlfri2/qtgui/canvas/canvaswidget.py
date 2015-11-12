from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter
from umlfri2.model.connection import ConnectionVisual
from umlfri2.model.element import ElementVisual
from umlfri2.qtgui.canvas.qtpaintercanvas import QTPainterCanvas
from umlfri2.qtgui.canvas.qtruler import QTRuler
from umlfri2.types.geometry import Point


class CanvasWidget(QWidget):
    def __init__(self, tab):
        super().__init__()
        self.__ruler = QTRuler()
        self.__tab = tab
        self.setFocusPolicy(Qt.StrongFocus)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        self.__tab.draw(canvas)
        painter.end()
    
    def get_ruler(self):
        return self.__ruler
    
    def mousePressEvent(self, event):
        # TODO: for testing purposes only
        pos = event.pos()
        object = self.__tab.diagram.get_object_at(self.__ruler, Point(pos.x(), pos.y()))
        if isinstance(object, ElementVisual):
            print('{0} at position {1}, {2}'.format(
                object.object.get_display_name(),
                pos.x(), pos.y())
            )
        elif isinstance(object, ConnectionVisual):
            print('{0}=>{1} at position {2}, {3}'.format(
                object.object.source.get_display_name(),
                object.object.destination.get_display_name(),
                pos.x(), pos.y())
            )
        else:
            print('None at position {0}, {1}'.format(pos.x(), pos.y()))
