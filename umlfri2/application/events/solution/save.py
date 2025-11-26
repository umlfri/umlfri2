from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.model import Solution


class SaveSolutionEvent(Event):
    def __init__(self, solution: Solution) -> None:
        self.__solution = solution
    
    @property
    def solution(self) -> Solution:
        return self.__solution
