from PyQt5.QtCore import QSize
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class AddOnsDialog:
    def __init__(self, main_window: UmlFriMainWindow) -> None: ...
    def sizeHint(self) -> QSize: ...
