from .infowidget import AddOnInfoWidget as AddOnInfoWidget
from PyQt5.QtWidgets import QDialog
from umlfri2.qtgui.base.hlinewidget import HLineWidget as HLineWidget

class InstallAddOnDialog(QDialog):
    TIMEOUT: int
    def __init__(self, addon_window, online_addon) -> None: ...
