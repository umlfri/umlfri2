from functools import partial

from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMenu, QAction

from umlfri2.application import Application
from umlfri2.qtgui.base import image_loader


class ContextMenu(QMenu):
    def _add_menu_item(self, icon, label, shortcut, action=None, sub_menu=None):
        ret = QAction(label, sub_menu or self)
        
        if shortcut is not None:
            ret.setShortcut(QKeySequence(shortcut))
        
        if isinstance(icon, str):
            ret.setIcon(QIcon.fromTheme(icon))
        elif isinstance(icon, QIcon):
            ret.setIcon(icon)
        
        if action is None:
            ret.setEnabled(False)
        else:
            ret.triggered.connect(action)
        
        (sub_menu or self).addAction(ret)
        
        return ret
    
    def _add_type_menu_item(self, type, action=None, sub_menu=None, format="{0}"):
        translation = type.metamodel.get_translation(Application().language.current_language)
        
        ret = QAction(format.format(translation.translate(type)), sub_menu or self)
        
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
