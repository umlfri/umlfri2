from .state import AddOnState


class AddOnStarter:
    class __StartErrorException(Exception):
        pass
    
    def __init__(self, manager, *addons):
        self.__manager = manager
        self.__addons = addons
        self.__started = False
        self.__has_error = False
        
        self.__dependencies = {}

        for addon in self.__manager:
            for provision in addon.provisions:
                self.__dependencies.setdefault(provision, []).append(addon)


    @property
    def finished(self):
        return self.__started
    
    @property
    def has_error(self):
        return self.__has_error
    
    def do(self):
        all_started = True
        for addon in self.__addons:
            try:
                started = self.__recursive_start(addon)
                all_started = all_started and started
            except AddOnStarter.__StartErrorException:
                self.__has_error = True
        
        self.__started = all_started

    def __recursive_start(self, addon):
        if addon.state != AddOnState.stopped:
            if addon.state == AddOnState.error:
                raise AddOnStarter.__StartErrorException()
            return addon.state in (AddOnState.started, AddOnState.none)
        
        dependencies_started = True
        
        for requirement in addon.requirements:
            for dependency in self.__dependencies.get(requirement):
                started = self.__recursive_start(dependency)
                dependencies_started = dependencies_started and started
        
        if dependencies_started:
            addon._start()
            if addon.state == AddOnState.error:
                raise AddOnStarter.__StartErrorException()
            return addon.state == AddOnState.started
        else:
            return False
