from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, cast

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
    def run(self, bookmark_idx: int) -> None:
        all_bookmarks = cast(List[Dict[str, Any]], hh_setting("bookmarks"))
        try:
            bookmark = all_bookmarks[bookmark_idx]
        except IndexError:
            return log("Bookmark index was out of range", status=True)

        pkg = cast(Optional[str], bookmark.get("package"))
        topic = cast(Optional[str], bookmark.get("topic"))
        caret = cast(Optional[Tuple[int, int]], bookmark.get("caret"))
        viewport = cast(Optional[Tuple[float, float]], bookmark.get("viewport"))

        if pkg is None or topic is None:
            return log("Bookmark at index specified is not valid", status=True)

        if show_help_topic(pkg, topic, history=True) == "file":
            help_view = find_help_view()
            if help_view is None:
                return

            if caret is not None:
                help_view.sel().clear()
                help_view.sel().add(sublime.Region(caret[0], caret[1]))

                if viewport is not None:
                    help_view.set_viewport_position(viewport, True)
                else:
                    help_view.show_at_center(help_view.sel()[0])

    def description(self, bookmark_idx: Optional[int] = None) -> str:
        if bookmark_idx is None:
            return "Invalid Bookmark Index"

        bmark = _bookmark_at_index(bookmark_idx)
        return (_bookmark_name(bmark) if bmark is not None
                                      else "Invalid Bookmark Index")

    def input(self, args: Dict[str, sublime.Value]) -> Optional[sublime_plugin.CommandInputHandler]:
        if args.get("bookmark_idx") is None:
            return BookmarkIdxInputHandler()

        return None


###----------------------------------------------------------------------------
