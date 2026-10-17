import sublime
import sublime_plugin

from .common import BookmarkTypeInputHandler, BookmarkNameInputHandler

from ...helpcore.common import current_help_file, current_help_package
from ...helpcore.view import find_help_view
from ...helpcore.core import help_index_list
from ...helpcore.help import _get_link_topic


###----------------------------------------------------------------------------


class HyperhelpPromptCreateBookmarkCommand(sublime_plugin.ApplicationCommand):
    """
    Interactively prompt the user to create a bookmark, asking them if they
    want to bookmark the current file, the current viewport or the topic that
    the link under the cursor would display.

    This invokes the actual command to create a bookmark if the user follows
    all interctive prompts.
    """
    def run(self, bmark_type, bmark_name):
        v = find_help_view(sublime.active_window())

        link_info = None
        if len(v.sel()) > 0 and v.match_selector(v.sel()[0].b, "meta.link"):
            link_info = _get_link_topic(v, v.extract_scope(v.sel()[0].b))

        pkg_name = current_help_package()
        topic = current_help_file()

        if bmark_type == "topic" and link_info is not None:
            pkg_name = link_info["pkg"]
            topic = link_info["topic"]

        caret = (v.sel()[0].a, v.sel()[0].b) if bmark_type == "view" else None
        viewport = v.viewport_position() if bmark_type == "view" else None

        sublime.run_command("hyperhelp_create_bookmark", {
            "name": bmark_name,
            "package": pkg_name,
            "topic": topic,
            "caret": caret,
            "viewport": viewport
            })

    def is_enabled(self, *kwargs):
        window = sublime.active_window()
        current_view = window.active_view() if window is not None else None
        help_view = find_help_view(window)

        return (current_view == help_view and
                current_view is not None and
                help_index_list().get(current_help_package()) is not None)

    def input_description(self):
        return "Create Bookmark"

    def input(self, args):
        bmark_type = args.get("bmark_type")
        if bmark_type is None:
            return BookmarkTypeInputHandler(find_help_view())

        if args.get("bmark_name") is None:
            return BookmarkNameInputHandler(find_help_view(), bmark_type)


###----------------------------------------------------------------------------
