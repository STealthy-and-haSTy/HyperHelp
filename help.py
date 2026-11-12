from __future__ import annotations

from typing import Optional, Sequence

import sublime  # noqa: F401

import importlib
import sys


###----------------------------------------------------------------------------


def reload(prefix: str, modules: Optional[Sequence[str]] = None) -> None:
    modules = [""] if modules is None else modules
    prefix = "HyperHelp.%s." % prefix

    for module in modules:
        module = (prefix + module).rstrip(".")
        if module in sys.modules:
            importlib.reload(sys.modules[module])


###----------------------------------------------------------------------------


reload("src")


# Import all of the commands, event listeners and such.
from .src import *

from .src import common


###----------------------------------------------------------------------------


def plugin_loaded() -> None:
    common.loaded()


def plugin_unloaded() -> None:
    common.unloaded()


###----------------------------------------------------------------------------
