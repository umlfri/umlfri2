from umlfri2.application.events.solution import CloseSolutionEvent
from .events.model import DiagramDeletedEvent
from .events.tabs import OpenTabEvent, ChangedCurrentTabEvent, ClosedTabEvent
from .tab import Tab


class TabList:
    def __init__(self, application):
        self.__tabs = []
        self.__application = application
        self.__current_tab = None
        self.__locked_tabs = set()
        
        application.event_dispatcher.subscribe(DiagramDeletedEvent, self.__diagram_deleted)
        application.event_dispatcher.subscribe(CloseSolutionEvent, self.__solution_closed)
    
    def __diagram_deleted(self, event):
        tab = self.get_tab_for(event.diagram)
        if tab is not None:
            tab.close()
    
    def __solution_closed(self, event):
        events = []

        for tab in self.__tabs:
            events.append(ClosedTabEvent(tab))

        self.__application.event_dispatcher.dispatch_all(events)
        self.__current_tab = None
        self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(None))
    
    def reset_lock_status(self):
        self.__locked_tabs = {tab.drawing_area.diagram.save_id for tab in self.__tabs if tab.locked}
    
    @property
    def lock_status_changed(self):
        new_locked_tabs = {tab.drawing_area.diagram.save_id for tab in self.__tabs if tab.locked}
        
        return self.__locked_tabs != new_locked_tabs
    
    def get_tab_for(self, diagram):
        for tab in self.__tabs:
            if tab.drawing_area.diagram is diagram:
                return tab
        
        return None
    
    def open_new_project_tabs(self, tabs):
        last_tab = None
        
        for tab_info in tabs:
            tab = Tab(self.__application, self, tab_info.diagram, locked=tab_info.locked)
            self.__tabs.append(tab)
            self.__application.event_dispatcher.dispatch(OpenTabEvent(tab))
            last_tab = tab
        
        if last_tab is not None:
            self.__current_tab = last_tab
            self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(last_tab))
    
    def select_tab(self, diagram):
        if diagram is None:
            self.__current_tab = None
            self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(None))
            return
        
        for tab in self.__tabs:
            if tab.drawing_area.diagram is diagram:
                if self.__current_tab is not tab:
                    self.__current_tab = tab
                    self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(tab))
                return tab
        else:
            tab = Tab(self.__application, self, diagram)
            self.__tabs.append(tab)
            self.__current_tab = tab
            self.__application.event_dispatcher.dispatch(OpenTabEvent(tab))
            self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(tab))
            return tab
    
    def _close_tab(self, tab):
        if tab.locked:
            tab.unlock()
        tab_id = self.__tabs.index(tab)
        del self.__tabs[tab_id]

        if tab_id < len(self.__tabs):
            self.__current_tab = self.__tabs[tab_id]
        elif self.__tabs:
            self.__current_tab = self.__tabs[-1]
        else:
            self.__current_tab = None

        self.__application.event_dispatcher.dispatch(ClosedTabEvent(tab))
        self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(self.__current_tab))
    
    def close_all(self):
        events = []
        new_tabs = []
        
        for tab in self.__tabs:
            if tab.locked:
                new_tabs.append(tab)
            else:
                events.append(ClosedTabEvent(tab))
        
        self.__tabs = new_tabs
        self.__application.event_dispatcher.dispatch_all(events)
        if new_tabs:
            self.__current_tab = new_tabs[-1]
            self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(new_tabs[-1]))
        else:
            self.__current_tab = None
            self.__application.event_dispatcher.dispatch(ChangedCurrentTabEvent(None))
    
    @property
    def current_tab(self):
        return self.__current_tab
    
    def __iter__(self):
        yield from self.__tabs
