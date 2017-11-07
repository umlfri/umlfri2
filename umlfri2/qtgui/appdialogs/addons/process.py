from PyQt5.QtCore import QTimer, Qt


class AddOnProcessManager:
    def __init__(self, dialog):
        self.__dialog = dialog
        self.__process = None
        self.__timer = QTimer(self.__dialog)
        self.__timer.timeout.connect(self.__timer_event)
    
    def run_process(self, process):
        self.__process = process
        self.__timer.start(100)
        self.__timer_event()
        self.__dialog.setEnabled(False)
        self.__dialog.setCursor(Qt.BusyCursor)
    
    def __timer_event(self):
        if self.__process.finished or self.__process.has_error:
            self.__timer.stop()
            self.__dialog.setEnabled(True)
            self.__dialog.unsetCursor()
            self.__process = None
        else:
            self.__process.do()
