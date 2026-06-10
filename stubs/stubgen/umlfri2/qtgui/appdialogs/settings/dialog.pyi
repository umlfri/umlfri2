from .general import SettingsDialogGeneral as SettingsDialogGeneral
from .updates import SettingsDialogUpdates as SettingsDialogUpdates
from PyQt5.QtWidgets import QDialog
from umlfri2.application import Application as Application
from umlfri2.application.events.application import LanguageChangedEvent as LanguageChangedEvent

class SettingsDialog(QDialog):
    def __init__(self, main_window) -> None: ...
