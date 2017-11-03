from collections import namedtuple
from uuid import UUID

from ...constants import MODEL_SCHEMA, MODEL_NAMESPACE

StartupTab = namedtuple('StartupTab', ['diagram', 'locked'])


class LockedTabsLoader:
    def __init__(self, xmlroot, all_diagrams):
        self.__xmlroot = xmlroot
        self.__all_diagrams = all_diagrams
        
        if not MODEL_SCHEMA.validate(self.__xmlroot):
            raise Exception("Cannot load project: {0}".format(MODEL_SCHEMA.error_log.last_error))
    
    def load(self):
        ret = []
        for node in self.__xmlroot:
            if node.tag == "{{{0}}}Tab".format(MODEL_NAMESPACE):
                ret.append(StartupTab(
                    self.__all_diagrams[UUID(node.attrib["diagram"])],
                    node.attrib["locked"].lower() in ("1", "true")
                ))

        return ret
