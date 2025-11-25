from __future__ import annotations

from typing import Optional, Tuple


class Event:
    def get_chained(self) -> Tuple[Event, ...]:
        return ()
    
    def get_opposite(self) -> Optional[Event]:
        return None
