import sublime
import sublime_plugin

from ...helpcore.view import find_help_view
from ...helpcore.core import show_help_topic
from ...helpcore.help import _get_link_topic


###----------------------------------------------------------------------------


class HyperhelpNavigateCommand(sublime_plugin.WindowCommand):
    """
    Perform navigation from within a help file
    """
    available_nav = ["find_anchor", "follow_link"]

    def run(self, nav, prev=False):
        if nav == "find_anchor":
            return self.anchor_nav(prev)
        else:
            return self.follow_link()

    def is_enabled(self, nav, prev=False):
        help_view = find_help_view()
        if help_view is None or nav not in self.available_nav:
            return False

        return True

    def anchor_nav(self, prev):
        help_view = find_help_view()
        anchors = help_view.get_regions("_hh_anchors")
        if not anchors:
            return

        point = help_view.sel()[0].begin()
        fallback = anchors[-1] if prev else anchors[0]

        pick = lambda p: (point < p.a) if not prev else (point > p.a)
        for pos in reversed(anchors) if prev else anchors:
            if pick(pos):
                return help_view.run_command("hyperhelp_focus",
                    {"position": [pos.b, pos.a]})

        help_view.run_command("hyperhelp_focus",
            {"position": [fallback.b, fallback.a]})

    def follow_link(self):
        help_view = find_help_view()
        point = help_view.sel()[0].begin()

        if help_view.match_selector(point, "text.hyperhelp meta.link"):
            topic = "_broken"
            package = help_view.settings().get("_hh_pkg")

            link_region = help_view.extract_scope(point)
            topic_dat = _get_link_topic(help_view, link_region)
            if topic_dat is not None:
                topic = topic_dat["topic"]
                package = topic_dat["pkg"] or package

            show_help_topic(package, topic, history=True)


###----------------------------------------------------------------------------
