from PySide.QtCore import Qt, QSize, QPoint
from PySide.QtGui import QWidget, QPainter, QApplication, QMenu, QContextMenuEvent
from umlfri2.application import Application
from umlfri2.application.commands.diagram import ShowElementCommand
from umlfri2.application.drawingarea import DrawingAreaCursor
from umlfri2.application.events.diagram import DiagramChangedEvent, SelectionChangedEvent
from umlfri2.application.events.model import ObjectChangedEvent
from umlfri2.model import ElementObject
from .menu import CanvasContextMenu
from ..mainwindow.projecttree import ProjectMimeData
from ..properties import PropertiesDialog
from .qtpaintercanvas import QTPainterCanvas
from umlfri2.types.geometry import Point


class CanvasWidget(QWidget):
    def __init__(self, main_window, drawing_area):
        super().__init__()
        self.__main_window = main_window
        self.__drawing_area = drawing_area
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.__old_cursor = None
        self.setAcceptDrops(True)
        self.__update_size()
        self.__mouse_down = False
        
        Application().event_dispatcher.subscribe(ObjectChangedEvent, self.__something_changed)
        Application().event_dispatcher.subscribe(DiagramChangedEvent, self.__something_changed)
        Application().event_dispatcher.subscribe(SelectionChangedEvent, self.__something_changed)
    
    @property
    def diagram(self):
        return self.__drawing_area.diagram
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas = QTPainterCanvas(painter)
        self.__drawing_area.draw(canvas)
        painter.end()

    def mousePressEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        if event.button() == Qt.LeftButton:
            self.__drawing_area.mouse_down(
                point,
                QApplication.keyboardModifiers() == Qt.ControlModifier,
                QApplication.keyboardModifiers() == Qt.ShiftModifier
            )
            
            self.__mouse_down = True
            
            self.__do_update()
        else:
            if self.__mouse_down:
                self.mouseReleaseEvent(event)
            
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        self.__drawing_area.mouse_move(
            point,
            QApplication.keyboardModifiers() == Qt.ControlModifier,
            QApplication.keyboardModifiers() == Qt.ShiftModifier
        )
        
        if self.__drawing_area.action_active:
            self.__do_update()
        else:
            self.__update_cursor()
    
    def mouseReleaseEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        if self.__mouse_down:
            self.__drawing_area.mouse_up(
                point,
                QApplication.keyboardModifiers() == Qt.ControlModifier,
                QApplication.keyboardModifiers() == Qt.ShiftModifier
            )
            
            self.__mouse_down = False
            
            self.__do_update()
        else:
            super().mousePressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        visual = self.__drawing_area.selection.get_lonely_selected_visual()
        if visual is None:
            return
        
        if not visual.is_at_position(Application().ruler, point):
            return
        
        self.__drawing_area.set_action(None)
        self.unsetCursor()
        PropertiesDialog.open_for(self.__main_window, visual.object)
        
    def contextMenuEvent(self, event):
        if event.reason() == QContextMenuEvent.Mouse:
            pos = event.pos()
            point = Point(pos.x(), pos.y())
            if self.__drawing_area.selection.is_selection_at(point):
                self.__drawing_area.selection.select_at(point)
            
            menu_pos = event.globalPos()
        else:
            point = self.__drawing_area.selection.get_bounds().center
            menu_pos = self.mapToGlobal(QPoint(point.x, point.y))
        
        self.unsetCursor()
        
        CanvasContextMenu(self.__main_window, self.__drawing_area).exec_(menu_pos)
    
    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if isinstance(mime_data, ProjectMimeData) and isinstance(mime_data.model_object, ElementObject):
            if mime_data.model_object.project is self.diagram.parent.project:
                event.acceptProposedAction()
    
    def dropEvent(self, event):
        mime_data = event.mimeData()
        if isinstance(mime_data, ProjectMimeData) and isinstance(mime_data.model_object, ElementObject):
            pos = event.pos()
            point = Point(pos.x(), pos.y())
            element = mime_data.model_object
            command = ShowElementCommand(self.diagram, element, point)
            Application().commands.execute(command)
    
    def __do_update(self):
        self.update()
        self.__update_size()
        self.__update_cursor()
    
    def __update_size(self):
        size = self.__drawing_area.get_size(Application().ruler)
        self.setMinimumSize(QSize(size.width, size.height))
    
    def __update_cursor(self):
        if self.__old_cursor == self.__drawing_area.cursor:
            return
        
        if self.__drawing_area.cursor == DrawingAreaCursor.arrow:
            self.unsetCursor()
        elif self.__drawing_area.cursor == DrawingAreaCursor.move:
            self.setCursor(Qt.SizeAllCursor)
        elif self.__drawing_area.cursor == DrawingAreaCursor.main_diagonal_resize:
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.__drawing_area.cursor == DrawingAreaCursor.anti_diagonal_resize:
            self.setCursor(Qt.SizeBDiagCursor)
        elif self.__drawing_area.cursor == DrawingAreaCursor.vertical_resize:
            self.setCursor(Qt.SizeVerCursor)
        elif self.__drawing_area.cursor == DrawingAreaCursor.horizontal_resize:
            self.setCursor(Qt.SizeHorCursor)
        elif self.__drawing_area.cursor == DrawingAreaCursor.cross:
            self.setCursor(Qt.CrossCursor)
        
        self.__old_cursor = self.__drawing_area.cursor
    
    def __something_changed(self, event):
        self.__do_update()

