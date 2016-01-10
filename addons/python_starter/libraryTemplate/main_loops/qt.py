from queue import Queue

import sys
from PySide.QtCore import QThread, Signal
from PySide.QtGui import QApplication


class QtMainLoop(object):
    class __MainThread(QThread):
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
        
    def main_loop(self, serve_callback):
        self.__thread = self.__MainThread(serve_callback)
        self.__thread.start()
        
        self.__running = True
        self.__app.exec_()
        self.__running = False
            
    def call(self, callable, *args):
        pass
    
    def quit(self):
        self.__app.quit()
    
    def wait(self):
        self.__thread.wait(3000)
