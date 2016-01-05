from umlfri2.application import Application
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from .toolbox import ToolBox


class MainToolBox(ToolBox):
    def __init__(self):
        super().__init__(None)
        
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__current_tab_changed)
    
    def __current_tab_changed(self, event):
        if event.tab is None:
            self._fill(None)
        else:
            self._fill(event.tab.drawing_area)
