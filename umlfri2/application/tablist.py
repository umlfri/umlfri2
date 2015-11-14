from .events.tabs import OpenTabEvent, ChangedCurrentTabEvent
from .tab import Tab


class TabList:
    def __init__(self, application):
        self.__tabs = []
        self.__application = application
        self.__current_tab = None
    
    def open_tab(self, diagram):
        tab = Tab(self.__application, diagram)
        self.__tabs.append(tab)
        self.__application.event_dispatcher.dispatch(OpenTabEvent(tab))
        self.__current_tab = tab
    
    @property
    def current_tab(self):
        return self.__current_tab
    
    @current_tab.setter
    def current_tab(self, value):
        self.__current_tab = value
        self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(value))
    
    def __iter__(self):
        yield from self.__tabs
