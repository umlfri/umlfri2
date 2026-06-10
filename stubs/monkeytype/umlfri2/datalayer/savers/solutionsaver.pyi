from umlfri2.datalayer.storages.zip import ZipStorage
from umlfri2.model.solution import Solution


class SolutionSaver:
    def __init__(self, storage: ZipStorage, path: str) -> None: ...
    def save(self, solution: Solution) -> None: ...
