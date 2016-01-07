import os.path

from umlfri2.plugin.starters import STARTER_LIST


class Plugin:
    def __init__(self, addon_path, starter, path):
        self.__addon_path = addon_path
        self.__starter = starter
        self.__path = path
        self.__addon = None
        self.__started_starter = None
    
    def _set_addon(self, addon):
        self.__addon = addon
    
    @property
    def is_running(self):
        return self.__started_starter is not None and self.__started_starter.is_alive
    
    def start(self):
        starter = STARTER_LIST[self.__starter]
        self.__started_starter = starter(os.path.join(self.__addon_path, self.__path))
        channel = self.__started_starter.start()
    
    def stop(self):
        pass
    
    def terminate(self):
        self.__started_starter.terminate()
    
    def kill(self):
        self.__started_starter.kill()
