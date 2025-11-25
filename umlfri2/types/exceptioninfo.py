from __future__ import annotations

import os.path
import sys
import traceback
from typing import Iterator, List, NamedTuple, Optional

from umlfri2.constants.paths import ROOT_DIR


class ExceptionInfoLine(NamedTuple):
    filename: Optional[str]
    module: Optional[str]
    lineno: int
    function: str
    text: Optional[str]


class ExceptionInfo:
    def __init__(self, type_name: str, description: str, traceback: List[ExceptionInfoLine],
                 cause: Optional[ExceptionInfo] = None, context: Optional[ExceptionInfo] = None) -> None:
        self.__type_name = type_name
        self.__description = description
        self.__traceback = traceback
        self.__cause = cause
        self.__context = context

    @staticmethod
    def from_exception(exception: BaseException) -> ExceptionInfo:
        if exception.__cause__ is not None:
            cause: Optional[ExceptionInfo] = ExceptionInfo.from_exception(exception.__cause__)
            context: Optional[ExceptionInfo] = None
        elif exception.__context__ is not None:
            cause = None
            context = ExceptionInfo.from_exception(exception.__context__)
        else:
            cause = None
            context = None
        
        tb: List[ExceptionInfoLine] = []
        for filename, lineno, function, text in traceback.extract_tb(exception.__traceback__):
            module = ExceptionInfo.__path_to_module(filename)
            
            if module is None:
                if filename.startswith(ROOT_DIR):
                    filename = filename[len(ROOT_DIR) + 1:]
                tb.append(ExceptionInfoLine(filename, None, lineno, function, text))
            else:
                tb.append(ExceptionInfoLine(None, module, lineno, function, text))
        
        type_name = type(exception).__name__
        desc = str(exception)
        
        return ExceptionInfo(type_name, desc, tb, cause, context)
    
    @staticmethod
    def __path_to_module(path: str) -> Optional[str]:
        try:
            npath = os.path.normpath(path)
        except:
            return None

        for name, module in sys.modules.items():
            if hasattr(module, '__file__'):
                try:
                    mpath = os.path.normpath(module.__file__)
                except:
                    continue

                if mpath == npath:
                    return name

        return None
    
    @property
    def type_name(self) -> str:
        return self.__type_name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def traceback(self) -> Iterator[ExceptionInfoLine]:
        yield from self.__traceback
    
    @property
    def cause(self) -> Optional[ExceptionInfo]:
        return self.__cause
    
    @property
    def context(self) -> Optional[ExceptionInfo]:
        return self.__context
