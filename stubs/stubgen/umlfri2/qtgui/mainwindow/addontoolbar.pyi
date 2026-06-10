from PyQt5.QtWidgets import QToolBar
from umlfri2.application import Application as Application
from umlfri2.application.events.addon import ActionEnableStatusChangedEvent as ActionEnableStatusChangedEvent
from umlfri2.qtgui.base import image_loader as image_loader

class AddOnToolBar(QToolBar):
    def __init__(self, toolbar) -> None: ...
    @property
    def toolbar(self): ...
