import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication


class QtMainLoop:
    class __MainThread(QThread):
        call = pyqtSignal(object, object)
        
        def __init__(self, callback):
            super().__init__()
            self.__callback = callback
        
        def run(self):
            self.__callback()
    
    def __init__(self):
        self.__running = False
        self.__app = QApplication(sys.argv)
    
    @property
    def in_main_loop(self):
        return self.__running
    
    def start(self, serve_callback):
        self.__thread = self.__MainThread(serve_callback)
        self.__thread.call.connect(lambda callable, args: callable(**args))
        self.__thread.start()
    
    def main_loop(self):
        self.__running = True
        self.__app.exec_()
        self.__running = False
            
    def call(self, callable, args):
        self.__thread.call.emit(callable, args)
    
    def quit(self):
        self.__app.quit()
    
    def wait(self):
        self.__thread.wait(3000)
