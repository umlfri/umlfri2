from PyQt5.QtCore import pyqtSignal, QThread, QObject

from umlfri2.application.threadmanager import ThreadManager


class QTThreadManager(QObject, ThreadManager):
    class __Thread(QThread):
        def __init__(self, callback):
            super().__init__()
            self.__callback = callback
        
        def run(self):
            self.__callback()
    
    __execute = pyqtSignal(object, object)
    
    def __init__(self):
        super().__init__()
        self.__thread = self.thread()
        self.__execute.connect(lambda function, args: function(*args))
    
    def execute_in_main_thread(self, function, *args):
        if QThread.currentThread() is self.__thread:
            function(*args)
        else:
            self.__execute.emit(function, args)

    def start_thread(self, function):
        thread = self.__Thread(function)
        thread.start()
        return thread
