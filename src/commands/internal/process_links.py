from __future__ import annotations

from typing import List, cast

import sublime
import sublime_plugin

from .common import _can_post_process

from ....helpcore.core import parse_link_body
from ....helpcore.common import current_help_package
from ....helpcore.data import LinkInfo


###----------------------------------------------------------------------------


class HyperhelpInternalProcessLinksCommand(sublime_plugin.TextCommand):
    """
    Process all links in a newly loaded help file. This does the work of
    rewriting links so that only their link text appears, while keeping track
    of the topic ID and package designations of each link.

    This results in regions and settings being applied to the view that allow
    the help core to navigate within the file.
    """
    def run(self, edit: sublime.Edit) -> None:
        v = self.view
        regions = v.find_by_selector("meta.link")
        default_pkg = current_help_package(self.view)

        v.add_regions("_hh_links", regions, "",
                      flags=sublime.HIDDEN | sublime.PERSISTENT)


        hh_links: List[LinkInfo] = [{"pkg": None, "topic": ""} for _ in regions]
        for idx, region in enumerate(reversed(regions)):
            base_text = v.substr(region)
            pkg_name, topic, text = parse_link_body(base_text)
            pkg_name = pkg_name or default_pkg

            if text is None:
                topic = "_broken"
                text = base_text
            elif topic is None:
                topic = "_broken"

            v.replace(edit, region, text)
            hh_links[len(regions) - idx - 1] = {
                "pkg": pkg_name,
                "topic": topic
            }

        v.settings().set("_hh_links", cast(sublime.ValueLike, hh_links))

        v.run_command("hyperhelp_internal_flag_links")

    def is_enabled(self) -> bool:
        return _can_post_process(self.view)


###----------------------------------------------------------------------------
