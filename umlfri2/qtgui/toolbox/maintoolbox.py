import sip

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QWIDGETSIZE_MAX

from umlfri2.application import Application
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from .expandbutton import ExpandButton
from .toolbox import ToolBox


class MainToolBox(QWidget):
    def __init__(self, dock):
        super().__init__()
        
        self.__dock = dock
        self.__empty_title_bar = QWidget()
        
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__expander = ExpandButton()
        self.__expander.expanded_changed.connect(self.__expander_changed)
        
        self.__toolbox = None
        
        self.__layout.addStretch()
        
        self.__change_toolbox(None)
        
        self.__layout.addWidget(self.__expander)
        
        self.setLayout(self.__layout)
        
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__current_tab_changed)
    
    @property
    def expanded(self):
        return self.__expander.expanded
    
    @expanded.setter
    def expanded(self, value):
        self.__expander.expanded = value
    
    def __current_tab_changed(self, event):
        if event.tab is None:
            self.__change_toolbox(None)
        else:
            self.__change_toolbox(event.tab.drawing_area)
    
    def __change_toolbox(self, drawing_area):
        if self.__toolbox is not None:
            self.__layout.removeWidget(self.__toolbox)
            sip.delete(self.__toolbox)
        
        self.setMinimumWidth(0)
        self.setMaximumWidth(QWIDGETSIZE_MAX)

        self.__toolbox = ToolBox(drawing_area, self.__expander.expanded)

        self.__layout.insertWidget(0, self.__toolbox)
        
        if not self.__expander.expanded:
            foo = self.__toolbox.sizeHint()
            self.setFixedWidth(foo.width())
            self.__dock.setTitleBarWidget(self.__empty_title_bar)
        else:
            self.__dock.setTitleBarWidget(None)
    
    def __expander_changed(self):
        self.__change_toolbox(self.__toolbox.drawing_area)
