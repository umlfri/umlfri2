from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from umlfri2.constants.keys import FULL_SCREEN
from .toolbox import ToolBox


class FullScreenToolBox(QWidget):
    close_clicked = pyqtSignal()
    
    def __init__(self, drawing_area):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__toolbox = ToolBox(drawing_area, False)
        self.__layout.addWidget(self.__toolbox)
        
        self.__close_button = QPushButton()
        self.__close_button.setIcon(QIcon.fromTheme("window-close"))
        self.__close_button.clicked.connect(self.__closed_clicked)
        self.__close_button.setToolTip(_("Exit fullscreen") + " ({0})".format(FULL_SCREEN))
        
        self.__layout.addStretch()
        
        self.__layout.addWidget(self.__close_button)
        
        self.setLayout(self.__layout)
    
    def __closed_clicked(self, checked=False):
        self.close_clicked.emit()
