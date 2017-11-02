from collections import namedtuple

import itertools

from ..state import AddOnState


class AddOnStopper:
    class __StopErrorException(Exception):
        pass
    
    __AddonWithDep = namedtuple('AddonDependency', ['addon', 'dependencies'])

    def __init__(self, manager, *addons):
        self.__manager = manager
        self.__stopped = False
        self.__has_error = False
        
        self.__reverse_dependencies = {}

        for addon in self.__manager:
            for requirement in addon.requirements:
                self.__reverse_dependencies.setdefault(requirement, []).append(addon)
        
        self.__addons = self.__recursive_compute_deps(addons)
    
    def __recursive_compute_deps(self, addons):
        ret = []
        
        for addon in addons:
            if addon.state in (AddOnState.stopped, AddOnState.none):
                continue

            deps = itertools.chain(*(self.__reverse_dependencies.get(provision, ()) for provision in addon.provisions))
            
            ret.append(
                self.__AddonWithDep(addon, self.__recursive_compute_deps(deps))
            )
        
        return ret

    @property
    def finished(self):
        return self.__stopped

    @property
    def has_error(self):
        return self.__has_error
    
    def addons(self):
        return set(*self.__iterate_addons(self.__addons))
    
    def __iterate_addons(self, addons):
        for addon_with_dep in addons:
            yield addon_with_dep.addon
            yield from self.__iterate_addons(addon_with_dep.dependencies)

    def do(self):
        all_stopped = True
        for addon in self.__addons:
            try:
                stopped = self.__recursive_stop(addon)
                all_stopped = all_stopped and stopped
            except AddOnStopper.__StopErrorException:
                self.__has_error = True
        
        self.__stopped = all_stopped

    def __recursive_stop(self, addon_with_dep):
        if addon_with_dep.addon.state != AddOnState.started:
            if addon_with_dep.addon.state == AddOnState.error:
                raise AddOnStopper.__StopErrorException()
            return addon_with_dep.addon.state in (AddOnState.stopped, AddOnState.error)
        
        dependencies_stopped = True
        
        for dep in addon_with_dep.dependencies:
            stopped = self.__recursive_stop(dep)
            dependencies_stopped = dependencies_stopped and stopped
        
        if dependencies_stopped:
            addon_with_dep.addon._stop()
            return addon_with_dep.addon.state in (AddOnState.stopped, AddOnState.error)
        else:
            return False
