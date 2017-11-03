from collections import namedtuple

from ...constants import MODEL_SCHEMA, MODEL_NAMESPACE

ProjectInfo = namedtuple("ProjectInfo", ["id"])
SolutionInfo = namedtuple("SolutionInfo", ["id", "projects"])


class SolutionInfoLoader:
    def __init__(self, xmlroot):
        self.__xmlroot = xmlroot
        
        if not MODEL_SCHEMA.validate(self.__xmlroot):
            raise Exception("Cannot load project: {0}".format(MODEL_SCHEMA.error_log.last_error))
    
    def load(self):
        ret = []
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Project".format(MODEL_NAMESPACE):
                ret.append(ProjectInfo(node.attrib["id"]))
        
        return SolutionInfo(self.__xmlroot.attrib["id"], ret)
