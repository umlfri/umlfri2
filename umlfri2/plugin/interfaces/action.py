from umlfri2.application.events.application import ActionTriggeredEvent
from .interface import Interface


class IAction(Interface):
    def __init__(self, executor, action):
        super().__init__(executor)
        self.__action = self._ref(action)

    @property
    def id(self):
        return 'action:{0}'.format(self.__action().id)

    @property
    def api_name(self):
        return 'Action'

    def get_enabled(self):
        return self.__action().enabled

    def set_enabled(self, value: bool):
        self.__action().enabled = value

    def get_id(self):
        return self.__action().id

    def register_triggered(self):
        self._application.event_dispatcher.subscribe(ActionTriggeredEvent, self.__fire_triggered)

    def deregister_triggered(self):
        self._application.event_dispatcher.unsubscribe(ActionTriggeredEvent, self.__fire_triggered)
    
    def __fire_triggered(self, event):
        if event.action is self.__action():
            self._executor.fire_event(self, 'triggered')
