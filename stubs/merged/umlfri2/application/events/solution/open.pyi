from ..base import Event as Event
from umlfri2.model.solution import Solution


class OpenSolutionEvent(Event):
    def __init__(self, solution: Solution) -> None: ...
    @property
    def solution(self): ...
