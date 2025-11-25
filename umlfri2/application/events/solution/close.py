from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Solution


class CloseSolutionEvent(Event):
    def __init__(self, solution: Optional[Solution]) -> None:
        self.__solution = solution

    @property
    def solution(self) -> Optional[Solution]:
        return self.__solution
