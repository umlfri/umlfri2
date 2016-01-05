from PySide.QtGui import QWidget, QHBoxLayout, QApplication, QShortcut, QKeySequence

from umlfri2.qtgui.canvas import ScrolledCanvasWidget
from umlfri2.qtgui.toolbox import ToolBox


class FullScreenDiagram(QWidget):
    def __init__(self, drawing_area):
        super().__init__()
        layout = QHBoxLayout()
        toolbox = ToolBox(drawing_area)
        layout.addWidget(toolbox)
        canvas = ScrolledCanvasWidget(self, drawing_area)
        layout.addWidget(canvas)
        self.setLayout(layout)
        
        QApplication.instance().focusChanged.connect(self.__focus_changed)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.__esc)
    
    def __focus_changed(self, old, new):
        if not self.isAncestorOf(new):
            self.close()
    
    def __esc(self):
        self.close()
