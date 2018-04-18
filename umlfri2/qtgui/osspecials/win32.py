import ctypes
from PyQt5.QtGui import QIcon

from umlfri2.constants.paths import OS_SPECIFIC_ICON_THEME_PATH
from umlfri2.application import Application

from .base import OSSpecials


NT_ICON_THEME = 'oxygen'


class Win32Specials(OSSpecials):
    def __apply_icons(self):
        QIcon.setThemeSearchPaths([OS_SPECIFIC_ICON_THEME_PATH])
        QIcon.setThemeName(NT_ICON_THEME)
    
    def __apply_model_id(self):
        SetCurrentProcessExplicitAppUserModelID = getattr(ctypes.windll.shell32, 'SetCurrentProcessExplicitAppUserModelID', None)
        
        if SetCurrentProcessExplicitAppUserModelID is not None:
            SetCurrentProcessExplicitAppUserModelID("FriUniza.UmlFri.{0}".format(Application().about.version.major_minor_string))
    
    def init(self):
        self.__apply_icons()
        self.__apply_model_id()
