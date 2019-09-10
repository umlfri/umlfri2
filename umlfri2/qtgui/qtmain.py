from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from umlfri2.application import Application

from .splashscreen import SplashScreen
from .base.qtthreadmanager import QTThreadManager
from .exceptionhook import install_exception_hook
from .rendering import QTRuler
from .osspecials import SPECIALS


def qt_main(args):
    SPECIALS.init()
    
    if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
        QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(args)
    
    Application().use_args(args[1:])

    Application().use_thread_manager(QTThreadManager())
    Application().use_ruler(QTRuler())

    Application().start()

    install_exception_hook()

    splash = SplashScreen()

    splash.start()

    SPECIALS.before_start()
    
    no = app.exec_()
    
    SPECIALS.after_quit()

    Application().stop()

    return no
