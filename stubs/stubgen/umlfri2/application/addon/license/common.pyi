from _typeshed import Incomplete
from typing import NamedTuple

def osi_license_url(abbreviation): ...

class CommonLicense:

    class __LicenseDescription(NamedTuple):
        title: Incomplete
        url: Incomplete
        abbreviation: Incomplete
    def __init__(self, abbreviation) -> None: ...
    @property
    def abbreviation(self): ...
    @property
    def title(self): ...
    @property
    def url(self): ...
