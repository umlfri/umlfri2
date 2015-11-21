from .events.tabs import OpenTabEvent, ChangedCurrentTabEvent, ClosedTabEvent
from .tab import Tab


class TabList:
    def __init__(self, application):
        self.__tabs = []
        self.__application = application
        self.__current_tab = None
    
    def select_tab(self, diagram):
        for tab in self.__tabs:
            if tab.drawing_area.diagram is diagram:
                if self.__current_tab is not tab:
                    self.__current_tab = tab
                    self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(tab))
                break
        else:
            tab = Tab(self.__application, diagram)
            self.__tabs.append(tab)
            self.__current_tab = tab
            self.__application.event_dispatcher.dispatch(OpenTabEvent(tab))
            self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(tab))
    
    def close_tab(self, diagram):
        for tab_id, tab in enumerate(self.__tabs):
            if tab.drawing_area.diagram is diagram:
                del self.__tabs[tab_id]
                
                if tab_id < len(self.__tabs):
                    self.__current_tab = self.__tabs[tab_id]
                elif self.__tabs:
                    self.__current_tab = self.__tabs[-1]
                else:
                    self.__current_tab = None
                
                self.__application.event_dispatcher.dispatch(ClosedTabEvent(tab))
                self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(self.__current_tab))
                break
    
    @property
    def current_tab(self):
        return self.__current_tab
    
    def __iter__(self):
        yield from self.__tabs
