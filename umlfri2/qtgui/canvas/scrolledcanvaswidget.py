from PySide.QtGui import QScrollArea, QFrame
from .canvaswidget import CanvasWidget


class ScrolledCanvasWidget(QScrollArea):
    def __init__(self, main_window, drawing_area):
        super().__init__()
        
        self.__canvas = CanvasWidget(main_window, drawing_area)
        
        self.setWidget(self.__canvas)
        self.setWidgetResizable(True)
    
    @property
    def diagram(self):
        return self.__canvas.diagram
