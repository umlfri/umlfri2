from ..base import Event


class CloseSolutionEvent(Event):
    def __init__(self, solution):
        self.__solution = solution

    @property
    def solution(self):
        return self.__solution
