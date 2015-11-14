from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter, QApplication

from umlfri2.application.drawingarea import DrawingAreaCursor
from .qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry import Point


class CanvasWidget(QWidget):
    def __init__(self, tab):
        super().__init__()
        self.__tab = tab
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.__old_cursor = None
    
    @property
    def tab(self):
        return self.__tab
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        self.__tab.drawing_area.draw(canvas)
        painter.end()

    def mousePressEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        self.__tab.drawing_area.mouse_down(point, QApplication.keyboardModifiers() == Qt.ControlModifier)
        
        self.__update_cursor()
        self.update()
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        self.__tab.drawing_area.mouse_move(point)
        
        self.__update_cursor()
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.__tab.drawing_area.mouse_up()
        self.update()
    
    def __update_cursor(self):
        if self.__old_cursor == self.__tab.drawing_area.cursor:
            return
        
        if self.__tab.drawing_area.cursor == DrawingAreaCursor.arrow:
            self.unsetCursor()
        elif self.__tab.drawing_area.cursor == DrawingAreaCursor.move:
            self.setCursor(Qt.SizeAllCursor)
        elif self.__tab.drawing_area.cursor == DrawingAreaCursor.mainDiagonalResize:
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.__tab.drawing_area.cursor == DrawingAreaCursor.antiDiagonalResize:
            self.setCursor(Qt.SizeBDiagCursor)
        elif self.__tab.drawing_area.cursor == DrawingAreaCursor.verticalResize:
            self.setCursor(Qt.SizeVerCursor)
        elif self.__tab.drawing_area.cursor == DrawingAreaCursor.horizontalResize:
            self.setCursor(Qt.SizeHorCursor)
        
        self.__old_cursor = self.__tab.drawing_area.cursor
