import sublime

import imp
import sys


###----------------------------------------------------------------------------


def reload(prefix, modules=[""]):
    prefix = "HyperHelp.%s." % prefix

    for module in modules:
        module = (prefix + module).rstrip(".")
        if module in sys.modules:
            imp.reload(sys.modules[module])


###----------------------------------------------------------------------------


reload("src")


# Import all of the commands, event listeners and such.
from .src import *


###----------------------------------------------------------------------------


def plugin_loaded():
    common.loaded()


def plugin_unloaded():
    common.unloaded()


###----------------------------------------------------------------------------
