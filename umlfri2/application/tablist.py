from .events.tabs import OpenTabEvent, ChangedCurrentTabEvent
from .tab import Tab


class TabList:
    def __init__(self, application):
        self.__tabs = []
        self.__application = application
        self.__current_tab = None
    
    def select_tab(self, diagram):
        for tab in self.__tabs:
            if tab.drawing_area.diagram is diagram:
                self.__current_tab = tab
                self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(tab))
                break
        else:
            tab = Tab(self.__application, diagram)
            self.__tabs.append(tab)
            self.__application.event_dispatcher.dispatch(OpenTabEvent(tab))
            self.__current_tab = tab
    
    @property
    def current_tab(self):
        return self.__current_tab
    
    def __iter__(self):
        yield from self.__tabs
