try:
    from PyQt5.QtPrintSupport import QPageSetupDialog, QPrinter, QPrinterInfo

    CAN_PRINT = True
except ImportError:
    CAN_PRINT = False

if CAN_PRINT:
    from .diagramprinting import DiagramPrinting


class MetaPrinting(type):
    __instance = None

    def __call__(cls):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls)

        return cls.__instance


class Printing(metaclass=MetaPrinting):
    def __init__(self):
        self.__printer = QPrinter(QPrinterInfo.defaultPrinter())
    
    @property
    def printer(self):
        return self.__printer

    def for_diagram(self, diagram):
        if not CAN_PRINT:
            raise Exception("Cannot print, Qt has no printing support")
        return DiagramPrinting(self, diagram)
    
    def show_page_setup(self):
        if not CAN_PRINT:
            raise Exception("Cannot print, Qt has no printing support")
        dlg = QPageSetupDialog(self.__printer)
        dlg.exec_()

    @property
    def can_print(self):
        return CAN_PRINT
