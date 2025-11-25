from __future__ import annotations

from typing import Any, Callable


class ThreadManager:
    def start_thread(self, function: Callable[[], None]) -> object:
        """
        Do not forget to keep returned reference. 
        """
        raise NotImplementedError
    
    def execute_in_main_thread(self, function: Callable[..., Any], *args: Any) -> None:
        raise NotImplementedError
