from io import (
    BufferedReader,
    BufferedWriter,
)
from typing import Dict


class FileChannel:
    def __init__(self, input: BufferedReader, output: BufferedWriter) -> None: ...
    @property
    def closed(self) -> bool: ...
    def write(self, data: Dict[str, str]) -> None: ...
