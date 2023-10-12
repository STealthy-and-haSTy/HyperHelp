### ---------------------------------------------------------------------------


__version_tuple = (0, 0, 8)
__version__ = ".".join([str(num) for num in __version_tuple])


### ---------------------------------------------------------------------------


__all__ = [
    "common",
    "core",
    "data",
    "help",
    "version"
    "view",
]


### ---------------------------------------------------------------------------


def version():
    """
    Get the version of the package as a tuple. This is used by the About
    command to display what version of the package is installed.
    """
    return __version_tuple


### ---------------------------------------------------------------------------