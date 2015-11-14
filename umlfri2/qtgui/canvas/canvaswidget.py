from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter, QApplication

from umlfri2.application.selection import ActionMoveSelection, ActionResizeElement, SelectionPointPosition, \
    ActionMoveConnectionPoint, ActionMoveLabel
from umlfri2.types.color import Colors
from ..base.qtruler import QTRuler
from .qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry import Point


class CanvasWidget(QWidget):
    SELECTION_RECTANGLE_FILL = Colors.blue.add_alpha(5)
    SELECTION_RECTANGLE_BORDER = Colors.blue
    SELECTION_RECTANGLE_WIDTH = 3
    
    def __init__(self, tab):
        super().__init__()
        self.__ruler = QTRuler()
        self.__tab = tab
        self.__postponed_action = None
        self.__current_action = None
        self.__current_action_point = None
        self.__current_action_bounds = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        self.__tab.draw(canvas)
        if self.__current_action is not None:
            if self.__current_action_bounds is not None:
                canvas.draw_rectangle(
                    self.__current_action_bounds,
                    self.SELECTION_RECTANGLE_BORDER,
                    self.SELECTION_RECTANGLE_FILL,
                    self.SELECTION_RECTANGLE_WIDTH
                )
        painter.end()
    
    def get_ruler(self):
        return self.__ruler

    def mousePressEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        action = self.__tab.selection.get_action_at(self.__ruler, point)
        
        if action is not None:
            self.__start_action(action, point)
        else:
            object = self.__tab.diagram.get_visual_at(self.__ruler, point)
            
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                if object is not None:
                    self.__tab.selection.toggle_select(object)
            else:
                self.__tab.selection.select(object)
                action = self.__tab.selection.get_action_at(self.__ruler, point)
                
                if action is not None:
                    self.__start_action(action, point)
                    self.__postpone_action()
        
        self.__change_cursor(point)
        
        self.update()
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        if not self.__is_in_action():
            if event.buttons() != Qt.NoButton:
                return
            
            self.__change_cursor(point)
        else:
            self.__process_action(point)
            self.update()
    
    def mouseReleaseEvent(self, event):
        if self.__is_in_action():
            self.__finish_action()
            self.update()

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
    
    def __start_action(self, action, point):
        self.__current_action = action
        if isinstance(self.__current_action, ActionMoveSelection):
            self.__current_action_bounds = self.__tab.selection.get_bounds(self.__ruler)
        
        self.__current_action_point = point
    
    def __is_in_action(self):
        return self.__current_action is not None or self.__postponed_action is not None
    
    def __postpone_action(self):
        self.__postponed_action = self.__current_action
        self.__current_action = None
    
    def __process_action(self, point):
        if self.__postponed_action is not None:
            self.__current_action = self.__postponed_action
            self.__postponed_action = None
        
        if isinstance(self.__current_action, ActionMoveSelection):
            self.__current_action_bounds += point - self.__current_action_point
        
        self.__current_action_point = point
    
    def __finish_action(self):
        if self.__postponed_action is not None:
            self.__postponed_action = None
        elif isinstance(self.__current_action, ActionMoveSelection):
            pass
        self.__current_action = None
        self.__current_action_bounds = None
