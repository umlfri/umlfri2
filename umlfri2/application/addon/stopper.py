from .state import AddOnState


class AddOnStopper:
    class __StopErrorException(Exception):
        pass

    def __init__(self, manager, *addons):
        self.__manager = manager
        self.__addons = addons
        self.__stopped = False
        self.__has_error = False

    @property
    def finished(self):
        return self.__stopped

    @property
    def has_error(self):
        return self.__has_error

    def do(self):
        reverse_dependencies = {}

        for addon in self.__addons:
            for requirement in addon.requirements:
                reverse_dependencies.setdefault(requirement, []).append(addon)

        all_stopped = True
        for addon in self.__addons:
            try:
                stopped = self.__recursion(reverse_dependencies, addon)
                all_stopped = all_stopped and stopped
            except AddOnStopper.__StopErrorException:
                self.__has_error = True

        self.__stopped = all_stopped

    def __recursion(self, reverse_dependencies, addon):
        if addon.state != AddOnState.started:
            if addon.state == AddOnState.error:
                raise AddOnStopper.__StopErrorException()
            return addon.state in (AddOnState.stopped, AddOnState.none)

        dependencies_stopped = True

        for provision in addon.provisions:
            for dependency in reverse_dependencies.get(provision):
                stopped = self.__recursion(reverse_dependencies, dependency)
                dependencies_stopped = dependencies_stopped and stopped

        if dependencies_stopped:
            addon._stop()
            if addon.state == AddOnState.error:
                raise AddOnStopper.__StopErrorException()
            return addon.state == AddOnState.stopped
        else:
            return False
