from PyQt5.QtGui import (
    QCloseEvent,
    QShowEvent,
)
from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class FullScreenDiagram:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        drawing_area: DrawingArea
    ) -> None: ...
    def closeEvent(self, event: QCloseEvent) -> None: ...
    def showEvent(self, event: QShowEvent) -> None: ...
