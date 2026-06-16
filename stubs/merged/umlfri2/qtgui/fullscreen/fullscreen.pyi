from PyQt5.QtGui import QKeySequence as QKeySequence
from PyQt5.QtWidgets import QWidget
from umlfri2.constants.keys import FULL_SCREEN as FULL_SCREEN
from umlfri2.qtgui.canvas import ScrolledCanvasWidget as ScrolledCanvasWidget
from umlfri2.qtgui.toolbox import FullScreenToolBox as FullScreenToolBox

class FullScreenDiagram(QWidget):
    def __init__(self, main_window, drawing_area) -> None: ...
    def showEvent(self, event) -> None: ...
    def closeEvent(self, event) -> None: ...
