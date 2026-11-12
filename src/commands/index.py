from __future__ import annotations

from typing import List, Optional

import sublime
import sublime_plugin

from ...helpcore.common import log, current_help_package, help_package_prompt
from ...helpcore.core import help_index_list
from ...helpcore.core import show_help_topic
from ...helpcore.data import HelpData, HelpTopic


###----------------------------------------------------------------------------


class HyperhelpIndexCommand(sublime_plugin.ApplicationCommand):
    """
    Display the index for the package provided. If no package is given and one
    cannot be inferred from the current help view, the user will be prompted to
    supply one. The prompt always occurs if the argument asks.
    """
    def run(self, package: Optional[str] = None,
            initial_text: Optional[str] = None,
            prompt: bool = False) -> None:
        package = package or current_help_package()
        if package is None or prompt:
            return help_package_prompt(help_index_list(),
                                       on_select=lambda pkg:
                                           self.run(pkg, initial_text))

        pkg_info = help_index_list().get(package, None)
        if pkg_info is None:
            return log("Cannot display topic index; unknown package '%s",
                       package, status=True)

        topics: List[HelpTopic] = [
            topic for topic in
            (pkg_info.help_topics.get(topic_name)
             for topic_name in sorted(pkg_info.help_topics.keys()))
            if topic is not None]

        items = [[t["caption"], t["topic"]]
                 for t in topics]

        if not items:
            return log("No help topics defined for package '%s'",
                       package, status=True)

        sublime.active_window().show_quick_panel(
            items,
            on_select=lambda index: self.select(pkg_info, items, index))

        if initial_text:
            sublime.active_window().run_command("insert", {"characters": initial_text})

    def is_enabled(self, package: Optional[str] = None,
                   prompt: bool = False) -> bool:
        if not prompt:
            package = package or current_help_package()
            if package is None:
                return False

        return True

    def select(self, pkg_info: HelpData, items: List[List[str]],
               index: int) -> None:
        if index >= 0:
            show_help_topic(pkg_info.package, items[index][1], history=True)


###----------------------------------------------------------------------------
