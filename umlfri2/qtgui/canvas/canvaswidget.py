from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter, QApplication

from umlfri2.application.selection import ActionMoveSelection, ActionResizeElement, SelectionPointPosition, \
    ActionMoveConnectionPoint, ActionMoveLabel
from ..base.qtruler import QTRuler
from .qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry import Point


class CanvasWidget(QWidget):
    def __init__(self, tab):
        super().__init__()
        self.__ruler = QTRuler()
        self.__tab = tab
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        self.__tab.draw(canvas)
        painter.end()
    
    def get_ruler(self):
        return self.__ruler
    
    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.NoButton:
            return
        
        pos = event.pos()

        self.__change_cursor(Point(pos.x(), pos.y()))

    def __change_cursor(self, point):
        action = self.__tab.selection.get_action_at(self.__ruler, point)
        if isinstance(action, ActionMoveSelection):
            self.setCursor(Qt.SizeAllCursor)
        elif isinstance(action, ActionResizeElement):
            if action.horizontal == SelectionPointPosition.first and action.vertical == SelectionPointPosition.first:
                self.setCursor(Qt.SizeFDiagCursor)
            elif action.horizontal == SelectionPointPosition.first and action.vertical == SelectionPointPosition.last:
                self.setCursor(Qt.SizeBDiagCursor)
            elif action.horizontal == SelectionPointPosition.last and action.vertical == SelectionPointPosition.first:
                self.setCursor(Qt.SizeBDiagCursor)
            elif action.horizontal == SelectionPointPosition.last and action.vertical == SelectionPointPosition.last:
                self.setCursor(Qt.SizeFDiagCursor)
            elif action.horizontal == SelectionPointPosition.center:
                self.setCursor(Qt.SizeVerCursor)
            elif action.vertical == SelectionPointPosition.center:
                self.setCursor(Qt.SizeHorCursor)
        elif isinstance(action, ActionMoveConnectionPoint):
            self.setCursor(Qt.SizeAllCursor)
        elif isinstance(action, ActionMoveLabel):
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.unsetCursor()

    def mousePressEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        object = self.__tab.diagram.get_visual_at(self.__ruler, point)
        
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if object is not None:
                self.__tab.selection.toggle_select(object)
        else:
            self.__tab.selection.select(object)
        
        self.__change_cursor(point)
        
        self.repaint()
