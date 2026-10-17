import sublime
import sublime_plugin

from .common import _can_post_process

from ....helpcore.core import parse_link_body
from ....helpcore.common import current_help_package


###----------------------------------------------------------------------------


class HyperhelpInternalProcessLinksCommand(sublime_plugin.TextCommand):
    """
    Process all links in a newly loaded help file. This does the work of
    rewriting links so that only their link text appears, while keeping track
    of the topic ID and package designations of each link.

    This results in regions and settings being applied to the view that allow
    the help core to navigate within the file.
    """
    def run(self, edit):
        v = self.view
        regions = v.find_by_selector("meta.link")
        default_pkg = current_help_package(self.view)

        v.add_regions("_hh_links", regions, "",
                      flags=sublime.HIDDEN | sublime.PERSISTENT)


        hh_links = [None] * len(regions)
        for idx,region in enumerate(reversed(regions)):
            base_text = v.substr(region)
            pkg_name, topic, text = parse_link_body(base_text)
            pkg_name = pkg_name or default_pkg

            if text is None:
                topic = "_broken"
                text = base_text

            v.replace(edit, region, text)
            hh_links[len(regions) - idx - 1] = {
                "pkg": pkg_name,
                "topic": topic
            }

        v.settings().set("_hh_links", hh_links)

        v.run_command("hyperhelp_internal_flag_links")

    def is_enabled(self):
        return _can_post_process(self.view)


###----------------------------------------------------------------------------
