from PyQt5.QtPrintSupport import QPrinter
from umlfri2.model.diagram import Diagram


class PagedRenderer:
    def __init__(self, device: QPrinter) -> None: ...
    def render_diagram(self, diagram: Diagram) -> None: ...
