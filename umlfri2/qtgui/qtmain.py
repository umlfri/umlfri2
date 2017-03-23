from PyQt5.QtWidgets import QApplication

from umlfri2.application import Application

from .splashscreen import SplashScreen
from .base.qtthreadmanager import QTThreadManager
from .exceptionhook import install_exception_hook
from .rendering import QTRuler
from .osspecials import apply_os_specials


def qt_main(args):
    apply_os_specials()

    app = QApplication(args)

    Application().use_thread_manager(QTThreadManager())
    Application().use_ruler(QTRuler())

    Application().start()

    install_exception_hook()

    splash = SplashScreen()

    splash.start()

    no = app.exec_()

    Application().stop()

    return no
