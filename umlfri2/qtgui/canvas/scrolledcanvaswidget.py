from PySide.QtCore import Qt
from PySide.QtGui import QScrollArea, QFrame, QWheelEvent
from .canvaswidget import CanvasWidget


class ScrolledCanvasWidget(QScrollArea):
    def __init__(self, main_window, drawing_area):
        super().__init__()
        
        self.__canvas = CanvasWidget(main_window, drawing_area)
        
        self.setWidget(self.__canvas)
        self.setWidgetResizable(True)
    
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            super().wheelEvent(QWheelEvent(event.pos(), event.delta(), event.buttons(), 0, Qt.Horizontal))
        else:
            super().wheelEvent(event)
    
    @property
    def diagram(self):
        return self.__canvas.diagram
