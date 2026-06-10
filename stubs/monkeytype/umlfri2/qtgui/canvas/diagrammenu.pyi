from umlfri2.application.drawingarea.drawingarea import DrawingArea
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class CanvasDiagramMenu:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        drawing_area: DrawingArea,
        diagram: Diagram
    ) -> None: ...
