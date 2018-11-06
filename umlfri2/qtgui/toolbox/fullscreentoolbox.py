from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .toolbox import ToolBox


class FullScreenToolBox(QWidget):
    def __init__(self, drawing_area):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__toolbox = ToolBox(drawing_area, False)
        self.__layout.addWidget(self.__toolbox)
        
        self.setLayout(self.__layout)
