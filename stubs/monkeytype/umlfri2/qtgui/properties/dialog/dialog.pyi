from PyQt5.QtCore import QSize
from typing import (
    Callable,
    Optional,
    Union,
)
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.model.project import Project
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow
from umlfri2.ufl.dialog.dialog import UflDialog


class PropertiesDialog:
    def __init__(
        self,
        main_window: UmlFriMainWindow,
        dialog: UflDialog,
        mk_apply_patch_command: Optional[Callable]
    ) -> None: ...
    @staticmethod
    def open_config(
        main_window: UmlFriMainWindow,
        project: Project
    ) -> None: ...
    @staticmethod
    def open_for(
        main_window: UmlFriMainWindow,
        object: Union[ConnectionObject, ElementObject]
    ) -> None: ...
    def sizeHint(self) -> QSize: ...
