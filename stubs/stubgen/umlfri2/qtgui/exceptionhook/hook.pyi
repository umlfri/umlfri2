from .dialog import ExceptionDialog as ExceptionDialog
from umlfri2.application import Application as Application

USE_SENTRY: bool

def exception_hook(exc_class, exc, tb) -> None: ...
def install_exception_hook() -> None: ...
