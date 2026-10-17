import sublime
import sublime_plugin

from .common import _can_post_process

from ....helpcore.core import parse_anchor_body


###----------------------------------------------------------------------------


class HyperhelpInternalProcessAnchorsCommand(sublime_plugin.TextCommand):
    """
    Process all anchors in a newly loaded help file. This does the work of
    rewriting anchors so that only their anchor text appears as well as
    removing the markup that makes hidden anchors hidden.

    This results in regions and settings being applied to the view that allow
    the help core to navigate within the file.
    """
    def run(self, edit):
        v = self.view
        v.add_regions("_hh_anchors", v.find_by_selector("meta.anchor"), "",
                     flags=sublime.HIDDEN | sublime.PERSISTENT)

        for pos in reversed(v.find_by_selector("punctuation.anchor.hidden")):
            v.erase(edit, pos)

        hh_nav = {}
        regions = v.get_regions("_hh_anchors")
        for idx, region in enumerate(reversed(regions)):
            topic, text = parse_anchor_body(v.substr(region))
            v.replace(edit, region, text)
            hh_nav[topic] = len(regions) - idx - 1

        v.settings().set("_hh_nav", hh_nav)

    def is_enabled(self):
        return _can_post_process(self.view)


###----------------------------------------------------------------------------
