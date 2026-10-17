import sublime
import sublime_plugin

from .common import _bookmark_at_index, _bookmark_name, BookmarkIdxInputHandler

from ...helpcore.common import log, hh_setting
from ...helpcore.view import find_help_view
from ...helpcore.core import show_help_topic


###----------------------------------------------------------------------------


class HyperhelpOpenBookmarkCommand(sublime_plugin.ApplicationCommand):
    """
    Navigate to a given bookmark for the user.
    """
    def run(self, bookmark_idx):
        all_bookmarks = hh_setting("bookmarks")
        try:
            bookmark = all_bookmarks[bookmark_idx]
        except IndexError:
            return log("Bookmark index was out of range", status=True)

        pkg = bookmark.get("package")
        topic = bookmark.get("topic")
        caret = bookmark.get("caret")
        viewport = bookmark.get("viewport")

        if pkg is None or topic is None:
            return log("Bookmark at index specified is not valid", status=True)

        if show_help_topic(pkg, topic, history=True) == "file":
            help_view = find_help_view()
            if caret is not None:
                help_view.sel().clear()
                help_view.sel().add(sublime.Region(caret[0], caret[1]))

                if viewport is not None:
                    help_view.set_viewport_position(viewport, True)
                else:
                    help_view.show_at_center(help_view.sel()[0])

    def description(self, bookmark_idx=None):
        bmark = _bookmark_at_index(bookmark_idx)
        return (_bookmark_name(bmark) if bmark is not None
                                      else "Invalid Bookmark Index")

    def input(self, args):
        if args.get("bookmark_idx") is None:
            return BookmarkIdxInputHandler()


###----------------------------------------------------------------------------
