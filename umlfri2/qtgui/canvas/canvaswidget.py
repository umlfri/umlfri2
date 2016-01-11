from PySide.QtCore import Qt, QSize, QPoint
from PySide.QtGui import QWidget, QPainter, QApplication, QContextMenuEvent, QShortcut, QKeySequence
from umlfri2.application import Application
from umlfri2.application.commands.diagram import ShowElementCommand, ChangeZOrderCommand, ZOrderDirection, \
    HideElementsCommand, HideConnectionCommand
from umlfri2.application.commands.model import DeleteElementsCommand, DeleteConnectionCommand
from umlfri2.application.drawingarea import DrawingAreaCursor
from umlfri2.application.events.application import ZoomChangedEvent
from umlfri2.application.events.diagram import DiagramChangedEvent, SelectionChangedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent, ConnectionChangedEvent
from umlfri2.constants.keys import DELETE_FROM_PROJECT, Z_ORDER_RAISE, Z_ORDER_LOWER, Z_ORDER_TO_BOTTOM, Z_ORDER_TO_TOP
from umlfri2.model import ElementObject
from umlfri2.types.geometry import Point
from .connectionmenu import CanvasConnectionMenu
from .diagrammenu import CanvasDiagramMenu
from .elementmenu import CanvasElementMenu
from ..projecttree import ProjectMimeData
from ..properties import PropertiesDialog
from ..rendering import QTPainterCanvas


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
        
        Application().event_dispatcher.subscribe(ObjectDataChangedEvent, self.__something_changed)
        Application().event_dispatcher.subscribe(DiagramChangedEvent, self.__something_changed)
        Application().event_dispatcher.subscribe(SelectionChangedEvent, self.__something_changed)
        Application().event_dispatcher.subscribe(ConnectionChangedEvent, self.__something_changed)
        Application().event_dispatcher.subscribe(ZoomChangedEvent, self.__something_changed)
        
        QShortcut(QKeySequence(QKeySequence.Delete), self).activated.connect(self.__hide_object)
        QShortcut(QKeySequence(DELETE_FROM_PROJECT), self).activated.connect(self.__delete_object)
        QShortcut(QKeySequence(Z_ORDER_RAISE), self).activated.connect(self.__z_order_back)
        QShortcut(QKeySequence(Z_ORDER_LOWER), self).activated.connect(self.__z_order_forward)
        QShortcut(QKeySequence(Z_ORDER_TO_BOTTOM), self).activated.connect(self.__z_order_bottom)
        QShortcut(QKeySequence(Z_ORDER_TO_TOP), self).activated.connect(self.__z_order_top)
    
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
        
        if not visual.object.has_ufl_dialog:
            return
        
        self.__drawing_area.set_action(None)
        self.unsetCursor()
        PropertiesDialog.open_for(self.__main_window, visual.object)
    
    def wheelEvent(self, event):
        if event.orientation() == Qt.Vertical and event.modifiers() == Qt.ControlModifier:
            if event.delta() > 0:
                self.__drawing_area.zoom_in()
            else:
                self.__drawing_area.zoom_out()
        else:
            super().wheelEvent(event)
        
    def contextMenuEvent(self, event):
        if event.reason() == QContextMenuEvent.Mouse:
            pos = event.pos()
            point = Point(pos.x(), pos.y())
            
            self.__drawing_area.ensure_selection_at(point)
        
        self.unsetCursor()
        
        if self.__drawing_area.selection.is_element_selected:
            menu = CanvasElementMenu(self.__main_window, self.__drawing_area,
                                     self.__drawing_area.selection.selected_elements)
        elif self.__drawing_area.selection.is_connection_selected:
            menu = CanvasConnectionMenu(self.__main_window, self.__drawing_area,
                                        self.__drawing_area.selection.selected_connection)
        elif self.__drawing_area.selection.is_diagram_selected:
            menu = CanvasDiagramMenu(self.__main_window, self.__drawing_area,
                                     self.__drawing_area.selection.selected_diagram)
        else:
            raise Exception
        
        menu_pos = event.globalPos()
        menu.exec_(menu_pos)
    
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
    
    def __hide_object(self):
        if self.__drawing_area.selection.selected_elements:
            command = HideElementsCommand(self.__drawing_area.diagram, self.__drawing_area.selection.selected_elements)
            Application().commands.execute(command)
        elif self.__drawing_area.selection.selected_connection:
            command = HideConnectionCommand(self.__drawing_area.diagram,
                                            self.__drawing_area.selection.selected_connection)
            Application().commands.execute(command)
    
    def __delete_object(self):
        if self.__drawing_area.selection.selected_elements:
            command = DeleteElementsCommand(
                tuple(element.object for element in self.__drawing_area.selection.selected_elements)
            )
            Application().commands.execute(command)
        elif self.__drawing_area.selection.selected_connection:
            command = DeleteConnectionCommand(self.__drawing_area.selection.selected_connection)
            
            Application().commands.execute(command)
    
    def __z_order_back(self):
        if self.__drawing_area.selection.is_element_selected:
            command = ChangeZOrderCommand(self.__drawing_area.diagram, self.__drawing_area.selection.selected_elements,
                                          ZOrderDirection.bellow)
            Application().commands.execute(command)
    
    def __z_order_forward(self):
        if self.__drawing_area.selection.is_element_selected:
            command = ChangeZOrderCommand(self.__drawing_area.diagram, self.__drawing_area.selection.selected_elements,
                                          ZOrderDirection.above)
            Application().commands.execute(command)
    
    def __z_order_bottom(self):
        if self.__drawing_area.selection.is_element_selected:
            command = ChangeZOrderCommand(self.__drawing_area.diagram, self.__drawing_area.selection.selected_elements,
                                          ZOrderDirection.bottom)
            Application().commands.execute(command)
    
    def __z_order_top(self):
        if self.__drawing_area.selection.is_element_selected:
            command = ChangeZOrderCommand(self.__drawing_area.diagram, self.__drawing_area.selection.selected_elements,
                                          ZOrderDirection.top)
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

