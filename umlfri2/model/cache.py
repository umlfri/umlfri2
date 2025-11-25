from __future__ import annotations

from typing import Any, Callable, Optional
from weakref import WeakSet


class ModelTemporaryDataCache:
    def __init__(self, callback: Optional[Callable[..., None]]) -> None:
        self.__reverse_dependencies: WeakSet[ModelTemporaryDataCache] = WeakSet()
        self.__invalidated: bool = True
        self.__callback = callback
        self.__is_refreshing: bool = False
    
    def depend_on(self, cache: ModelTemporaryDataCache) -> None:
        cache.__reverse_dependencies.add(self)
    
    def invalidate(self) -> None:
        self.__invalidated = True
        for dependant in self.__reverse_dependencies:
            dependant.invalidate()
    
    def refresh(self, **kwargs: Any) -> None:
        self.__is_refreshing = True
        if self.__callback is not None:
            self.__callback(**kwargs)
        
        for dependant in self.__reverse_dependencies:
            dependant.invalidate()
        self.__invalidated = False
    
    def ensure_valid(self, **kwargs: Any) -> None:
        if self.__invalidated:
            self.refresh(**kwargs)
