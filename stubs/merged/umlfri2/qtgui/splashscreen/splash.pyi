from PyQt5.QtWidgets import QSplashScreen
from umlfri2.application import Application as Application
from umlfri2.constants.paths import GRAPHICS as GRAPHICS
from umlfri2.constants.splashscreen import SPLASH_TIMEOUT as SPLASH_TIMEOUT
from umlfri2.qtgui.mainwindow import UmlFriMainWindow as UmlFriMainWindow

class SplashScreen(QSplashScreen):
    def __init__(self) -> None: ...
    def start(self) -> None: ...
    def drawContents(self, painter) -> None: ...
