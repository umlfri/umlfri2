from functools import partial

from PySide.QtGui import QToolBar

from umlfri2.qtgui.base import image_loader


class AddOnToolBar(QToolBar):
    def __init__(self, toolbar):
        super().__init__()
        
        self.__toolbar = toolbar
        
        self.setWindowTitle(toolbar.label)
        
        for item in toolbar.items:
            qt_action = self.addAction(item.label)
            qt_action.setToolTip(item.label)
            if item.icon is not None:
                qt_action.setIcon(image_loader.load_icon(item.icon))
            qt_action.setEnabled(item.action.enabled)
            qt_action.triggered.connect(partial(self.__action, item.action))
    
    @property
    def toolbar(self):
        return self.__toolbar
    
    def __action(self, action, checked=False):
        action.trigger()
