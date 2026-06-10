from .expandbutton import ExpandButton as ExpandButton
from .toolbox import ToolBox as ToolBox
from PyQt5.QtWidgets import QWidget
from umlfri2.application import Application as Application
from umlfri2.application.events.tabs import ChangedCurrentTabEvent as ChangedCurrentTabEvent

class MainToolBox(QWidget):
    def __init__(self, dock) -> None: ...
    @property
    def expanded(self): ...
    @expanded.setter
    def expanded(self, value) -> None: ...
