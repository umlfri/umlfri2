from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QScrollArea

from .canvaswidget import CanvasWidget


class ScrolledCanvasWidget(QScrollArea):
    def __init__(self, main_window, drawing_area):
        super().__init__()
        
        self.__canvas = CanvasWidget(main_window, drawing_area)
        
        self.setWidget(self.__canvas)
        self.setWidgetResizable(True)
    
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            pixelDelta = event.pixelDelta()
            angleDelta = event.angleDelta()
            
            if angleDelta.x() == 0 and angleDelta.y() != 0:
                delta = angleDelta.y()
                orientation = Qt.Horizontal
            else:
                delta = angleDelta.x()
                orientation = Qt.Vertical
            
            super().wheelEvent(QWheelEvent(event.pos(), event.globalPos(),
                                           QPoint(pixelDelta.y(), pixelDelta.x()),
                                           QPoint(angleDelta.y(), angleDelta.x()),
                                           delta, orientation,
                                           event.buttons(), Qt.NoModifier))
        else:
            super().wheelEvent(event)
    
    @property
    def diagram(self):
        return self.__canvas.diagram
