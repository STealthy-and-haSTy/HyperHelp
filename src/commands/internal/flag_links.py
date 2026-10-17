import sublime
import sublime_plugin

from ....helpcore.core import help_index_list, lookup_help_topic
from ....helpcore.core import is_topic_file_valid
from ....helpcore.help import _get_link_topic


###----------------------------------------------------------------------------


class HyperhelpInternalFlagLinksCommand(sublime_plugin.TextCommand):
    """
    Given a help file which has had its links post processed already via
    hyperhelp_internal_process_links, this checks each link in the file and
    classifies them as either active or broken, depending on whether or not
    they point to a valid destination.

    This is a non-destructive command and may be executed any time the
    underlying help indexes may have changed, such as at Sublime startup.
    """
    def run(self, edit):
        v = self.view
        active = []
        broken = []

        regions = v.get_regions("_hh_links")
        for idx, region in enumerate(regions):
            link_dat = _get_link_topic(v, idx)

            pkg_info = help_index_list().get(link_dat["pkg"], None)
            topic = lookup_help_topic(pkg_info, link_dat["topic"])

            if self.link_is_active(pkg_info, topic):
                active.append(region)
            else:
                broken.append(region)

        v.add_regions("_hh_links_active", active, "storage",
            flags=sublime.DRAW_SOLID_UNDERLINE | sublime.PERSISTENT |
                  sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE)

        v.add_regions("_hh_links_broken", broken, "comment",
            flags=sublime.DRAW_STIPPLED_UNDERLINE | sublime.PERSISTENT |
                  sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE)

    def link_is_active(self, pkg_info, topic):
        if topic is None:
            return False

        # Returns None if the topic is not a file, so only consider the topic
        # broken when the return is definitely false.
        if is_topic_file_valid(pkg_info, topic) is False:
            return False

        return True

    def is_enabled(self):
        return self.view.match_selector(0, "text.hyperhelp.help")


###----------------------------------------------------------------------------
