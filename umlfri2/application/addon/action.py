from umlfri2.application.events.application import ActionTriggeredEvent, ActionEnableStatusChangedEvent


class AddOnAction:
    def __init__(self, application, id):
        self.__application = application
        self.__id = id
        self.__enabled = True
        self.__addon = None
    
    def _set_addon(self, addon):
        self.__addon = addon
    
    @property
    def id(self):
        return self.__id
    
    @property
    def addon(self):
        return self.__addon
    
    @property
    def enabled(self):
        return self.__enabled
    
    @enabled.setter
    def enabled(self, value):
        self.__enabled = value
        self.__application.event_dispatcher.dispatch(ActionEnableStatusChangedEvent(self))
    
    def trigger(self):
        self.__application.event_dispatcher.dispatch(ActionTriggeredEvent(self))
