from .state import AddOnState


class AddOnStarter:
    def __init__(self, manager, *addons):
        self.__manager = manager
        self.__addons = addons
        self.__started = False
    
    @property
    def finished(self):
        return self.__started
    
    def do(self):
        dependencies = {}

        for addon in self.__manager:
            for provision in addon.provisions:
                dependencies.setdefault(provision, []).append(addon)
        
        all_started = True
        for addon in self.__addons:
            started = self.__recursion(dependencies, addon)
            all_started = all_started and started
        
        self.__started = all_started

    def __recursion(self, dependencies, addon):
        if addon.state != AddOnState.stopped:
            return addon.state in (AddOnState.started, AddOnState.none)
        
        dependencies_started = True
        
        for requirement in addon.requirements:
            for dependency in dependencies.get(requirement):
                started = self.__recursion(dependencies, dependency)
                dependencies_started = dependencies_started and started
        
        if dependencies_started:
            addon._start()
            return addon.state == AddOnState.started
        else:
            return False
