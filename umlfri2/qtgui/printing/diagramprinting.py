from PyQt5.QtPrintSupport import QPrintDialog, QPrintPreviewDialog

from umlfri2.qtgui.rendering import PagedRenderer


class DiagramPrinting:
    def __init__(self, printing, diagram):
        self.__printing = printing
        self.__diagram = diagram
    
    def show_preview(self):
        dlg = QPrintPreviewDialog(self.__printing.printer)
        dlg.paintRequested.connect(self.__print_diagram)
        dlg.exec_()
    
    def print(self):
        dlg = QPrintDialog(self.__printing.printer)
        if dlg.exec_() == QPrintDialog.Accepted:
            self.__print_diagram(self.__printing.printer)
    
    def __print_diagram(self, printer):
        renderer = PagedRenderer(printer)
        renderer.render_diagram(self.__diagram)
