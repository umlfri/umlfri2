from PyQt5.QtCore import QSize
from umlfri2.model.project import Project
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow


class ProjectPropertiesDialog:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        project: Project
    ) -> None: ...
    @staticmethod
    def open_for(
        main_window: UmlFriMainWindow,
        project: Project
    ) -> None: ...
    @property
    def project_name(self) -> str: ...
    def sizeHint(self) -> QSize: ...
