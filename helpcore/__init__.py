from __future__ import annotations

### ---------------------------------------------------------------------------

from typing import List, Tuple

from . import common
from . import core
from . import data
from . import help
from . import view

__version_tuple: Tuple[int, int, int] = (0, 0, 9)
__version__: str = ".".join([str(num) for num in __version_tuple])


### ---------------------------------------------------------------------------


__all__: List[str] = [
    "common",
    "core",
    "data",
    "help",
    "version",
    "view",
]


### ---------------------------------------------------------------------------


def version() -> Tuple[int, int, int]:
    """
    Get the version of the installed dependency package as a tuple. This is
    used during the bootstrap check to see if the version of the dependency has
    changed.
    """
    return __version_tuple


### ---------------------------------------------------------------------------
