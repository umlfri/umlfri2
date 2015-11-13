from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter, QApplication
from ..base.qtruler import QTRuler
from .qtpaintercanvas import QTPainterCanvas
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
        pos = event.pos()
        object = self.__tab.diagram.get_visual_at(self.__ruler, Point(pos.x(), pos.y()))
        
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if object is not None:
                self.__tab.selection.toggle_select(object)
        else:
            self.__tab.selection.select(object)
        
        self.repaint()
