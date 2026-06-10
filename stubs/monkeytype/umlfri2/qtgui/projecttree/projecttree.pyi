from PyQt5.QtCore import Qt
from typing import List
from umlfri2.qtgui.mainwindow.mainwindow import UmlFriMainWindow
from umlfri2.qtgui.projecttree.mimedata import ProjectMimeData
from umlfri2.qtgui.projecttree.treeitem import ProjectTreeItem


class ProjectTree:
    def __init__(self, main_window: UmlFriMainWindow) -> None: ...
    def dropMimeData(
        self,
        parent: ProjectTreeItem,
        index: int,
        data: ProjectMimeData,
        action: Qt.DropAction
    ) -> bool: ...
    def mimeData(
        self,
        items: List[ProjectTreeItem]
    ) -> ProjectMimeData: ...
    def reload(self) -> None: ...
