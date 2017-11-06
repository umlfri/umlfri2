from PyQt5.QtCore import QTimer


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

    def __timer_event(self):
        if self.__process.finished:
            self.__timer.stop()
            self.__dialog.setEnabled(True)
        else:
            self.__process.do()
