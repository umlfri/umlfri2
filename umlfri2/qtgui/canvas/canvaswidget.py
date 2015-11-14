from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter, QApplication

from umlfri2.application import Application
from umlfri2.application.commands.diagram import MoveSelectionCommand
from umlfri2.application.commands.diagram.resizemoveelement import ResizeMoveElementCommand
from umlfri2.application.selection import ActionMoveSelection, ActionResizeElement, SelectionPointPosition, \
    ActionMoveConnectionPoint, ActionMoveLabel, ActionSelectMany
from umlfri2.types.color import Colors
from ..base.qtruler import QTRuler
from .qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry import Point, Rectangle


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
        self.setAttribute(Qt.WA_OpaquePaintEvent)
    
    @property
    def tab(self):
        return self.__tab
    
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
                
                if action is None:
                    action = ActionSelectMany()
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
        elif isinstance(self.__current_action, ActionResizeElement):
            self.__current_action_bounds = self.__current_action.element.get_bounds(self.__ruler)
        elif isinstance(self.__current_action, ActionSelectMany):
            self.__current_action_bounds = Rectangle.from_point_point(point, point)
        
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
        
        vector = point - self.__current_action_point
        
        if isinstance(self.__current_action, ActionMoveSelection):
            self.__current_action_bounds += vector
        elif isinstance(self.__current_action, ActionResizeElement):
            x1 = self.__current_action_bounds.x1
            y1 = self.__current_action_bounds.y1
            x2 = self.__current_action_bounds.x2
            y2 = self.__current_action_bounds.y2
            
            min_size = self.__current_action.element.get_minimal_size(self.__ruler)
            
            if self.__current_action.horizontal == SelectionPointPosition.first:
                x1 += vector.x
                if x2 - x1 < min_size.width:
                    x1 = x2 - min_size.width
            elif self.__current_action.horizontal == SelectionPointPosition.last:
                x2 += vector.x
                if x2 - x1 < min_size.width:
                    x2 = x1 + min_size.width
            
            if self.__current_action.vertical == SelectionPointPosition.first:
                y1 += vector.y
                if y2 - y1 < min_size.height:
                    y1 = y2 - min_size.height
            elif self.__current_action.vertical == SelectionPointPosition.last:
                y2 += vector.y
                if y2 - y1 < min_size.height:
                    y2 = y1 + min_size.height
            
            self.__current_action_bounds = Rectangle(x1, y1, x2 - x1, y2 - y1)
        elif isinstance(self.__current_action, ActionSelectMany):
            self.__current_action_bounds = Rectangle.from_point_point(self.__current_action_bounds.top_left, point)
        
        # TODO: don't move current point
        self.__current_action_point = point
    
    def __finish_action(self):
        if self.__postponed_action is not None:
            self.__postponed_action = None
        elif isinstance(self.__current_action, ActionMoveSelection):
            old_bounds = self.__tab.selection.get_bounds(self.__ruler)
            command = MoveSelectionCommand(
                self.__tab.selection,
                self.__current_action_bounds.top_left - old_bounds.top_left
            )
            Application().commands.execute(command)
        elif isinstance(self.__current_action, ActionResizeElement):
            command = ResizeMoveElementCommand(
                self.__current_action.element,
                self.__current_action_bounds
            )
            Application().commands.execute(command)
        elif isinstance(self.__current_action, ActionSelectMany):
            self.__tab.selection.select_in_area(self.__ruler, self.__current_action_bounds.normalize())
        
        self.__current_action = None
        self.__current_action_bounds = None
