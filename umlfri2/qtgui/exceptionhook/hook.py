import sys
import traceback

from umlfri2.application import Application
from .dialog import ExceptionDialog

try:
    import sentry_sdk
    import sentry_sdk.utils
    import sentry_sdk.hub
    
    USE_SENTRY = True
except ImportError:
    USE_SENTRY = False


def exception_hook(exc_class, exc, tb):
    if __debug__:
        traceback.print_exception(exc_class, exc, tb)
    elif USE_SENTRY:
        try:
            hub = sentry_sdk.hub.Hub.current
            with sentry_sdk.utils.capture_internal_exceptions():
                event, hint = sentry_sdk.utils.event_from_exception(
                    (exc_class, exc, tb),
                    client_options=hub.client.options,
                    mechanism={"type": "excepthook", "handled": False},
                )
                hub.capture_event(event, hint=hint)
        except Exception:
            pass
    
    dialog = ExceptionDialog(exc)
    dialog.exec_()


def install_exception_hook():
    global USE_SENTRY
    if USE_SENTRY:
        try:
            sentry_sdk.init(
                "https://08536bfb825c4333b17f474e87810875@sentry.io/1376591",
                release="umllfri2@{0}".format(Application().about.version)
            )
        except Exception:
            USE_SENTRY = False
            if __debug__:
                traceback.print_exc()
    sys.excepthook = exception_hook
