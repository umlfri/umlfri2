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
        self.__events = Queue()
        self.__running = False
    
    @property
    def in_main_loop(self):
        return self.__running
        
    def main_loop(self, serve_callback):
        self.__app = QApplication(sys.argv)
        self.__MainThread(serve_callback).start()
        
        self.__running = True
        while True:
            cmd = self.__events.get()
            if cmd is None:
                break
            cmd[0](*cmd[1])
        self.__running = False
            
    def call(self, callable, *args):
        self.__events.put((callable, args))
    
    def quit(self):
        self.__events.put(None)
