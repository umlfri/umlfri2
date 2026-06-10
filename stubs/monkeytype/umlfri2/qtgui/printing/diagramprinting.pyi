from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.printing.printing import Printing


class DiagramPrinting:
    def __init__(
        self,
        printing: Printing,
        diagram: Diagram
    ) -> None: ...
    def print(self) -> None: ...
