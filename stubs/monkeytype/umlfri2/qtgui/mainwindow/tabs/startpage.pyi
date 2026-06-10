from PyQt5.QtGui import QPaintEvent
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class StartPage:
    def __init__(self, main_window: UmlFriMainWindow) -> None: ...
    def paintEvent(self, event: QPaintEvent) -> None: ...
