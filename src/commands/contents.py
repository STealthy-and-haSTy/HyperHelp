from __future__ import annotations

from typing import List, Optional

import sublime
import sublime_plugin

from ...helpcore.common import log, help_package_prompt
from ...helpcore.common import current_help_package
from ...helpcore.core import help_index_list
from ...helpcore.core import show_help_topic
from ...helpcore.data import HelpData, HelpTocEntry


###----------------------------------------------------------------------------


class HyperhelpContentsCommand(sublime_plugin.ApplicationCommand):
    """
    Display the table of contents for the package provided. If no package is
    given and one cannot be inferred from the current help view, the user will
    be prompted to supply one. The prompt always occurs if the argument asks.
    """
    def run(self, package: Optional[str] = None,
            prompt: bool = False) -> None:
        package = package or current_help_package()
        if package is None or prompt:
            return help_package_prompt(help_index_list(),
                                       on_select=lambda pkg: self.run(pkg))

        pkg_info = help_index_list().get(package, None)
        if pkg_info is None:
            return log("Cannot display table of contents; unknown package '%s",
                       package, status=True)

        self.show_toc(pkg_info, pkg_info.help_toc, [])

    def is_enabled(self, package: Optional[str] = None,
                   prompt: bool = False) -> bool:
        if not prompt:
            package = package or current_help_package()
            if package is None:
                return False

        return True

    def show_toc(self, pkg_info: HelpData, items: List[HelpTocEntry],
                 stack: List[List[HelpTocEntry]]) -> None:
        captions = [[item["caption"], item["topic"] +
            (" ({} topics)".format(len(item["children"])) if "children" in item else "")]
            for item in items]

        if not captions and not stack:
            return log("No help topics defined for package '%s'",
                       pkg_info.package, status=True)

        if stack:
            captions.insert(0, ["..", "Go back"])

        sublime.active_window().show_quick_panel(
            captions,
            on_select=lambda index: self.select(pkg_info, items, stack, index))

    def select(self, pkg_info: HelpData, items: List[HelpTocEntry],
               stack: List[List[HelpTocEntry]], index: int) -> None:
        if index >= 0:
            # When the stack isn't empty, the first item takes us back.
            if index == 0 and len(stack) > 0:
                items = stack.pop()
                return self.show_toc(pkg_info, items, stack)

            # Compenstate for the "go back" item when the stack's not empty
            if len(stack) > 0:
                index -= 1

            entry = items[index]
            children = entry.get("children", None)

            if children is not None:
                stack.append(items)
                return self.show_toc(pkg_info, children, stack)

            show_help_topic(pkg_info.package, entry["topic"], history=True)


###----------------------------------------------------------------------------
