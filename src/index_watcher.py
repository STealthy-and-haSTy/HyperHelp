from __future__ import annotations

from typing import ClassVar, List, Optional, Set, cast

import sublime
import sublime_plugin  # noqa: F401

from ..helpcore.common import log
from ..helpcore.core import load_indexes_from_packages
from ..helpcore.core import unload_help_indexes_from_packges



###----------------------------------------------------------------------------


class PackageIndexWatcher():
    """
    A simple singleton class for determining when packages are being added to
    or removed from the list of ignored packages, so that we can trigger help
    indexes in those packages to be either unloaded or loaded, as needed.
    """
    instance: ClassVar[Optional["PackageIndexWatcher"]] = None

    def __init__(self) -> None:
        if PackageIndexWatcher.instance is not None:
            return

        PackageIndexWatcher.instance = self
        self.settings: sublime.Settings = sublime.load_settings(
            "Preferences.sublime-settings")
        self.cached_ignored: Set[str] = set(cast(
            List[str], self.settings.get("ignored_packages", [])))

        self.settings.add_on_change("_hh_sw", lambda: self.__setting_changed())

    @classmethod
    def unregister(cls) -> None:
        if PackageIndexWatcher.instance is not None:
            PackageIndexWatcher.instance.settings.clear_on_change("_hh_sw")
            PackageIndexWatcher.instance = None


    def __setting_changed(self) -> None:
        new_list: Set[str] = set(cast(
            List[str], self.settings.get("ignored_packages", [])))
        if new_list == self.cached_ignored:
            return

        removed = self.cached_ignored - new_list
        added = new_list - self.cached_ignored
        self.cached_ignored = new_list

        if added:
            log("unloading all help indexes loaded from: %s", list(added))
            sublime.set_timeout(
                lambda: unload_help_indexes_from_packges(list(added)), 2000)

        if removed:
            log("scanning for help indexes in: %s", list(removed))
            sublime.set_timeout(
                lambda: load_indexes_from_packages(list(removed)), 2000)


###----------------------------------------------------------------------------
