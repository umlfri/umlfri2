from .events.tabs import OpenTabEvent
from .tab import Tab


class TabList:
    def __init__(self, dispatcher):
        self.__tabs = []
        self.__dispatcher = dispatcher
        self.__current_tab = None
    
    def open_tab(self, diagram):
        tab = Tab(diagram)
        self.__tabs.append(tab)
        self.__dispatcher.dispatch(OpenTabEvent(tab))
        self.__current_tab = tab
    
    @property
    def current_tab(self):
        return self.__current_tab
    
    @current_tab.setter
    def current_tab(self, value):
        self.__current_tab = value
    
    def __iter__(self):
        yield from self.__tabs
