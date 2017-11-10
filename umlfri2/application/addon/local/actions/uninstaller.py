class AddOnUninstaller:
    def __init__(self, manager, addon):
        self.__manager = manager
        self.__addon = addon
        self.__addon_stopper = addon.stop()
        self.__finished = False
        self.__error = False
    
    @property
    def finished(self):
        return self.__finished
    
    @property
    def has_error(self):
        return self.__error
    
    def do(self):
        if self.__error or self.__finished:
            return
        
        if self.__addon_stopper is not None:
            try:
                self.__addon_stopper.do()
            except:
                self.__error = True
                raise
            if self.__addon_stopper.finished:
                self.__addon_stopper = None
        else:
            try:
                self.__manager.uninstall_addon(self.__addon)
            except:
                self.__error = True
                raise
            self.__finished = True
