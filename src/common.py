import sublime
import sublime_plugin

from .startup import post_install_update_check

from ..helpcore.view import find_help_view
from .index_watcher import PackageIndexWatcher


###----------------------------------------------------------------------------


def loaded():
    """
    Do package setup at package load time.
    """
    # If there is an existing help view in any of the open windows, ensure that
    # its links are properly underlined.
    for window in sublime.windows():
        view = find_help_view(window)
        if view:
            view.run_command("hyperhelp_internal_flag_links")

    # When we hook into the package control event system to track when we were
    # just installed or updated, it will insert a window setting that tells us
    # what topic we should display at start, for an install or update messge.
    post_install_update_check()

    # Start watching the list of ignored packages so that we have a hook into
    # packages that may have help being loaded or unloaded.
    PackageIndexWatcher()


def unloaded():
    """
    Do package cleanup at unload time.
    """
    PackageIndexWatcher.unregister()


###----------------------------------------------------------------------------
