from .startpage import StartPage as StartPage
from .tabbar import MiddleClosableTabBar as MiddleClosableTabBar
from .tabcontextmenu import TabContextMenu as TabContextMenu
from PyQt5.QtWidgets import QTabWidget
from umlfri2.application import Application as Application
from umlfri2.application.events.application import LanguageChangedEvent as LanguageChangedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent as ObjectDataChangedEvent
from umlfri2.application.events.tabs import ChangedCurrentTabEvent as ChangedCurrentTabEvent, ClosedTabEvent as ClosedTabEvent, OpenTabEvent as OpenTabEvent, TabLockStatusChangedEvent as TabLockStatusChangedEvent
from umlfri2.model import Diagram as Diagram
from umlfri2.qtgui.base import image_loader as image_loader
from umlfri2.qtgui.base.icon_combiner import combine_icons as combine_icons
from umlfri2.qtgui.base.resources import ICONS as ICONS
from umlfri2.qtgui.canvas import CanvasWidget as CanvasWidget, ScrolledCanvasWidget as ScrolledCanvasWidget

class Tabs(QTabWidget):
    def __init__(self, main_window) -> None: ...
