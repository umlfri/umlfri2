from PySide.QtGui import QMenu, QAction, QKeySequence, QIcon

from umlfri2.constants.keys import DELETE_FROM_PROJECT


class CanvasContextMenu(QMenu):
    def __init__(self, drawing_area):
        super().__init__()
        
        self.__drawing_area = drawing_area
        
        diagram = drawing_area.selection.is_diagram_selected
        
        self.__add_menu_item(None, _("Delete from diagram"), QKeySequence.Delete, not diagram)
        self.__add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, not diagram)

    def __add_menu_item(self, icon, label, shortcut, enabled=True, action=None):
        ret = QAction(label, self)
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        if action is not None:
            ret.triggered.connect(action)
        if not enabled:
            ret.setEnabled(False)
        self.addAction(ret)
        return ret
