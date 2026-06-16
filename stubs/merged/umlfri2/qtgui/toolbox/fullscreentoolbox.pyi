from .toolbox import ToolBox as ToolBox
from PyQt5.QtWidgets import QWidget
from _typeshed import Incomplete
from umlfri2.constants.keys import FULL_SCREEN as FULL_SCREEN

class FullScreenToolBox(QWidget):
    close_clicked: Incomplete
    def __init__(self, drawing_area) -> None: ...
