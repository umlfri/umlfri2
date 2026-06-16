from ...base.contextmenu import ContextMenu as ContextMenu
from .startpage import StartPage as StartPage
from umlfri2.application import Application as Application

class TabContextMenu(ContextMenu):
    def __init__(self, tab_bar, tab_index, tab_widget) -> None: ...
