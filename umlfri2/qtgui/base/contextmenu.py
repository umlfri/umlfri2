from functools import partial

from PySide.QtGui import QMenu, QIcon, QKeySequence, QAction

from umlfri2.application import Application
from umlfri2.qtgui.base import image_loader


class ContextMenu(QMenu):
    def _add_menu_item(self, icon, label, shortcut, action=None, sub_menu=None):
        ret = QAction(label, sub_menu or self)
        
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        
        if icon is not None:
            ret.setIcon(QIcon.fromTheme(icon))
        
        if action is None:
            ret.setEnabled(False)
        else:
            ret.triggered.connect(action)
        
        (sub_menu or self).addAction(ret)
        
        return ret
    
    def _add_type_menu_item(self, type, action=None, sub_menu=None):
        translation = type.metamodel.addon.get_translation(Application().language)
        
        ret = QAction(translation.translate(type), sub_menu or self)
        
        ret.setIcon(image_loader.load_icon(type.icon))
        
        if action is None:
            ret.setEnabled(False)
        else:
            ret.triggered.connect(partial(action, type))
        
        (sub_menu or self).addAction(ret)
        
        return ret
    
    def _add_sub_menu_item(self, label, enabled=True, sub_menu=None):
        ret = QAction(label, sub_menu or self)
        
        menu = QMenu()
        ret.setMenu(menu)
        
        ret.setEnabled(enabled)
        
        (sub_menu or self).addAction(ret)
        
        return menu