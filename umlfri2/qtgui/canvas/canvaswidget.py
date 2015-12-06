from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QPainter, QApplication

from umlfri2.application import Application
from umlfri2.application.commands.diagram import ShowElementCommand
from umlfri2.application.drawingarea import DrawingAreaCursor
from umlfri2.application.events.diagram import DiagramChangedEvent
from umlfri2.application.events.model import ObjectChangedEvent
from umlfri2.model import ElementObject
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
        Application().event_dispatcher.register(ObjectChangedEvent, self.__something_changed)
        Application().event_dispatcher.register(DiagramChangedEvent, self.__something_changed)
    
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
        
        self.__drawing_area.mouse_down(
            point,
            QApplication.keyboardModifiers() == Qt.ControlModifier,
            QApplication.keyboardModifiers() == Qt.ShiftModifier
        )
        
        self.__update_cursor()
        self.update()
    
    def mouseMoveEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        self.__drawing_area.mouse_move(
            point,
            QApplication.keyboardModifiers() == Qt.ControlModifier,
            QApplication.keyboardModifiers() == Qt.ShiftModifier
        )
        
        self.__update_cursor()
        self.update()
    
    def mouseReleaseEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        
        self.__drawing_area.mouse_up(
            point,
            QApplication.keyboardModifiers() == Qt.ControlModifier,
            QApplication.keyboardModifiers() == Qt.ShiftModifier
        )
        
        self.__update_cursor()
        self.update()
    
    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        point = Point(pos.x(), pos.y())
        object = self.__drawing_area.get_object_at(point)
        if object is not None:
            self.__drawing_area.set_action(None)
            self.unsetCursor()
            PropertiesDialog.open_for(self.__main_window, object)
    
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
        self.update()
