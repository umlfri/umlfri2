from ...constants import FRIP2_LOCKED_TABS_FILE as FRIP2_LOCKED_TABS_FILE, FRIP2_MIMETYPE_FILE as FRIP2_MIMETYPE_FILE, FRIP2_PROJECT_FILE as FRIP2_PROJECT_FILE, FRIP2_SOLUTION_FILE as FRIP2_SOLUTION_FILE, FRIP2_VERSION_FILE as FRIP2_VERSION_FILE, MODEL_SAVE_VERSION as MODEL_SAVE_VERSION, SOLUTION_MIME_TYPE as SOLUTION_MIME_TYPE
from .lockedtabsloader import LockedTabsLoader as LockedTabsLoader
from .projectloader import ProjectLoader as ProjectLoader
from .solutioninfoloader import SolutionInfoLoader as SolutionInfoLoader
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.model import Solution as Solution
from umlfri2.types.version import Version as Version

class WholeSolutionLoader:
    def __init__(self, storage, ruler, addon_manager) -> None: ...
    @property
    def solution(self): ...
    @property
    def locked_tabs(self) -> Generator[Incomplete, Incomplete]: ...
    def load(self) -> None: ...
    @staticmethod
    def is_valid_save(storage): ...
