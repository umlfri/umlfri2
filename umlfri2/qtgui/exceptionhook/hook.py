import sys
import traceback

from .dialog import ExceptionDialog


def exception_hook(exc_class, exc, tb):
    if __debug__:
        traceback.print_exception(exc_class, exc, tb)
    
    dialog = ExceptionDialog(exc)
    dialog.exec_()


def install_exception_hook():
    sys.excepthook = exception_hook
