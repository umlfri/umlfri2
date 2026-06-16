from PyQt5.QtCore import QEvent as QEvent
from PyQt5.QtWidgets import QWidget
from umlfri2.application import Application as Application
from umlfri2.application.drawingarea.actions import AddElementAction as AddElementAction, AddTypedConnectionAction as AddTypedConnectionAction
from umlfri2.application.events.application import LanguageChangedEvent as LanguageChangedEvent
from umlfri2.constants.paths import GRAPHICS as GRAPHICS
from umlfri2.qtgui.base import image_loader as image_loader
from umlfri2.qtgui.base.hlinewidget import HLineWidget as HLineWidget

class ToolBox(QWidget):
    def __init__(self, drawing_area, show_names) -> None: ...
    @property
    def drawing_area(self): ...
