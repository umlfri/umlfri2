from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class CanvasConnectionMenu:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        drawing_area: DrawingArea,
        connection: ConnectionVisual
    ) -> None: ...
