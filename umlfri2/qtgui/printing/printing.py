try:
    from PyQt5.QtPrintSupport import QPageSetupDialog, QPrinter, QPrinterInfo

    has_printing_support = True
except ImportError:
    has_printing_support = False

if has_printing_support:
    from .diagramprinting import DiagramPrinting


class MetaPrinting(type):
    __instance = None

    def __call__(cls):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls)

        return cls.__instance


class Printing(metaclass=MetaPrinting):
    def __init__(self):
        if has_printing_support:
            self.__printer = QPrinter(QPrinterInfo.defaultPrinter())
        else:
            self.__printer = None
    
    @property
    def printer(self):
        return self.__printer

    def for_diagram(self, diagram):
        if not has_printing_support:
            raise Exception("Cannot print, Qt has no printing support")
        return DiagramPrinting(self, diagram)
    
    def show_page_setup(self):
        if not has_printing_support:
            raise Exception("Cannot print, Qt has no printing support")
        dlg = QPageSetupDialog(self.__printer)
        dlg.exec_()
    
    @property
    def has_printing_support(self):
        return has_printing_support
    
    @property
    def can_print(self):
        return any(QPrinterInfo.availablePrinters())
