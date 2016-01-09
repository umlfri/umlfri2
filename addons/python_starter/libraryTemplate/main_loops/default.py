from queue import Queue
from threading import Thread


class DefaultMainLoop(object):
    def __init__(self):
        self.__events = Queue()
        self.__running = False
    
    @property
    def in_main_loop(self):
        return self.__running
        
    def main_loop(self, serve_callback):
        Thread(serve_callback, daemon=True).start()
        
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
