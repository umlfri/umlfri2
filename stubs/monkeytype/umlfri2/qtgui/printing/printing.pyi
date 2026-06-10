from PyQt5.QtPrintSupport import QPrinter
from umlfri2.model.diagram import Diagram
from umlfri2.qtgui.printing.diagramprinting import DiagramPrinting


class MetaPrinting:
    def __call__(cls) -> Printing: ...


class Printing:
    def __init__(self) -> None: ...
    @property
    def can_print(self) -> bool: ...
    def for_diagram(
        self,
        diagram: Diagram
    ) -> DiagramPrinting: ...
    @property
    def has_printing_support(self) -> bool: ...
    @property
    def printer(self) -> QPrinter: ...
