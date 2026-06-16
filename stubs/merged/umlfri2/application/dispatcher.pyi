from _weakref import ref
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Type,
)
from umlfri2.application.application import Application
from umlfri2.application.events.base.event import Event
from umlfri2.application.events.tabs.closed import ClosedTabEvent


class methodref(ref):
    def __new__(
        cls: Type[methodref],
        method: Callable,
        callback: None = None
    ) -> methodref: ...
    def __call__(self) -> Optional[Callable]: ...

class EventDispatcher:
    def __init__(self, application: Application) -> None: ...
    def subscribe(self, event_type: Any, function: Callable, auto_unsubscribe: bool = True) -> None: ...
    def unsubscribe(self, event_type, function) -> None: ...
    def dispatch(self, event: Event) -> None: ...
    def dispatch_all(self, events: List[ClosedTabEvent]) -> None: ...
    def clear(self) -> None: ...
