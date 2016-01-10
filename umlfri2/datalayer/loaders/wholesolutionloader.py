from uuid import UUID

import lxml.etree

from .projectloader import ProjectLoader
from ..constants import FRIP2_SOLUTION_FILE, FRIP2_PROJECT_FILE
from .solutioninfoloader import SolutionInfoLoader
from umlfri2.model import Solution


class WholeSolutionLoader:
    def __init__(self, storage, ruler, addon_manager):
        self.__storage = storage
        self.__ruler = ruler
        self.__addon_manager = addon_manager
    
    def load(self):
        solution_info = SolutionInfoLoader(lxml.etree.parse(self.__storage.open(FRIP2_SOLUTION_FILE)).getroot()).load()
        
        solution = Solution(save_id=UUID(solution_info.id))
        
        for project in solution_info.projects:
            project_xml = lxml.etree.parse(self.__storage.open(FRIP2_PROJECT_FILE.format(project.id))).getroot()
            solution.add_project(ProjectLoader(project_xml, self.__ruler, False,
                                               addon_manager=self.__addon_manager).load())
        
        return solution
