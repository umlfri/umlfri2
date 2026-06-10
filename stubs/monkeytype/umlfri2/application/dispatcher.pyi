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


class EventDispatcher:
    def __init__(self, application: Application) -> None: ...
    def clear(self) -> None: ...
    def dispatch(self, event: Event) -> None: ...
    def dispatch_all(self, events: List[ClosedTabEvent]) -> None: ...
    def subscribe(self, event_type: Any, function: Callable, auto_unsubscribe: bool = ...) -> None: ...


class methodref:
    def __call__(self) -> Optional[Callable]: ...
    @staticmethod
    def __new__(
        cls: Type[methodref],
        method: Callable,
        callback: None = ...
    ) -> methodref: ...
