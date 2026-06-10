from .base.qtthreadmanager import QTThreadManager as QTThreadManager
from .exceptionhook import install_exception_hook as install_exception_hook
from .osspecials import SPECIALS as SPECIALS
from .rendering import QTRuler as QTRuler
from .splashscreen import SplashScreen as SplashScreen
from umlfri2.application import Application as Application

def qt_main(args): ...
