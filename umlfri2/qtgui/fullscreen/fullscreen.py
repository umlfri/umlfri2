from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QShortcut

from umlfri2.qtgui.canvas import ScrolledCanvasWidget
from umlfri2.qtgui.toolbox import ToolBox


class FullScreenDiagram(QWidget):
    def __init__(self, main_window, drawing_area):
        super().__init__()
        self.__main_window = main_window
        
        layout = QHBoxLayout()
        toolbox = ToolBox(drawing_area)
        layout.addWidget(toolbox)
        canvas = ScrolledCanvasWidget(self, drawing_area)
        layout.addWidget(canvas)
        self.setLayout(layout)
        
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.__esc)

    def __esc(self):
        self.close()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.__main_window.setEnabled(False)
    
    def closeEvent(self, event):
        super().changeEvent(event)
        self.__main_window.setEnabled(True)
        
