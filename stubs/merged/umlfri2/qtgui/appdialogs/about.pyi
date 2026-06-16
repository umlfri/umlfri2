from PyQt5.QtWidgets import QDialog
from umlfri2.application import Application as Application
from umlfri2.application.events.application import UpdateCheckFinishedEvent as UpdateCheckFinishedEvent, UpdateCheckStartedEvent as UpdateCheckStartedEvent
from umlfri2.constants.paths import GRAPHICS as GRAPHICS, LICENSE_FILE as LICENSE_FILE
from umlfri2.qtgui.exceptionhook import ExceptionDialog as ExceptionDialog

class AboutDialog(QDialog):
    def __init__(self, main_window) -> None: ...
