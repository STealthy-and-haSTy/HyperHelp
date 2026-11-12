from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, cast

import sublime
import sublime_plugin

from ...helpcore.common import log, hh_setting, hh_update_setting
from ...helpcore.common import current_help_file, current_help_package
from ...helpcore.view import find_help_view
from ...helpcore.core import help_index_list, lookup_help_topic
from ...helpcore.help import _get_link_topic


###----------------------------------------------------------------------------


if TYPE_CHECKING:
    from sublime_types import Event

    class _StringListInputHandler(sublime_plugin.ListInputHandler[str]):
        pass

    class _IntListInputHandler(sublime_plugin.ListInputHandler[int]):
        pass
else:
    _StringListInputHandler = sublime_plugin.ListInputHandler
    _IntListInputHandler = sublime_plugin.ListInputHandler


###----------------------------------------------------------------------------


def _get_bookmarks() -> List[Dict[str, Any]]:
    """
    Get the list of user bookmarks from the settings file as a list of bookmark
    dictionaries. This list may be empty if the user has not defined any
    bookmarks yet.
    """
    return cast(List[Dict[str, Any]], hh_setting("bookmarks"))


def _add_bookmark(bookmark: Dict[str, Any]) -> None:
    """
    Given a valid bookmark dictionary, add it to the list of user bookmarks in
    the settings file.
    """
    bookmarks = _get_bookmarks()
    bookmarks.append(bookmark)
    hh_update_setting("bookmarks", bookmarks, save=True)


def _bookmark_name(bookmark: Optional[Dict[str, Any]]) -> str:
    """
    Given a bookmark dictionary, return back the name of that bookmark. If the
    bookmark has no defined name, one will be returned.
    """
    if bookmark is None:
        return "No bookmark"

    if "name" in bookmark:
        return str(bookmark["name"])

    package = bookmark.get("package")
    pkg_info = (help_index_list().get(package, None)
                if isinstance(package, str) else None)
    topic = lookup_help_topic(pkg_info, str(bookmark.get("topic", '')))

    if topic is None:
        return "Bookmark specifies invalid topic"

    if pkg_info is not None and topic["topic"] in pkg_info.help_files:
        return pkg_info.help_files[topic["topic"]]

    return topic.get("caption", "Caption is missing")



def _bookmark_at_index(bookmark_idx: int,
                       displayError: bool = False) -> Optional[Dict[str, Any]]:
    """
    Return the bookmark dictionary for the user bookmark at the given index, if
    any. None is returned if the index is invalid. The optional argument can be
    used to signal an error in the status line if the bookmark index is
    invalid.
    """
    all_bookmarks = _get_bookmarks()
    try:
        return all_bookmarks[bookmark_idx]

    except IndexError:
        if displayError:
            log("Bookmark index was out of range", status=True)

        return None


###----------------------------------------------------------------------------


class BookmarkIdxInputHandler(_IntListInputHandler):
    """
    Allow the user to select an appropriate bookmark index by displaying a list
    of all bookmarks by name.
    """
    def list_items(self) -> List[Tuple[str, int]]:
        return [(_bookmark_name(bmark), idx)
                for idx, bmark in enumerate(_get_bookmarks())]


class BookmarkTypeInputHandler(_StringListInputHandler):
    """
    Allow the user to select what type of bookmark they want to create by
    displaying a list of the available bookmark types that are valid in the
    current context.
    """
    names = {
        "file": "Current file",
        "topic": "Current topic",
        "view": "Current view"
    }
    descs = {
        "file": "Bookmark the current help file",
        "topic": "Bookmark the topic currently under the cursor",
        "view": "Bookmark the current help view"
    }

    def __init__(self, help_view: sublime.View) -> None:
        super().__init__()
        self.view = help_view
        self.bmark_type = ""

    def name(self) -> str:
        return "bmark_type"

    def placeholder(self) -> str:
        return "bookmark type"

    def preview(self, text: str) -> sublime.Html:
        return sublime.Html("<strong>{}</strong>: <em>{}</em>".format(
            self.names.get(text, "unknown"),
            self.descs.get(text, "unknown")
        ))

    def list_items(self) -> List[Tuple[str, str]]:
        items = [
            ("this file", "file"),
            ("this view", "view")
        ]

        if len(self.view.sel()) > 0:
            pt = self.view.sel()[0].b
            if self.view.match_selector(pt, "meta.link"):
                items.insert(1, ("this topic", "topic"))

        return items

    def validate(self, text: str, event: Optional[Event] = None) -> bool:
        self.bmark_type = text
        return True

    def next_input(self, args: Dict[str, sublime.Value]) -> Optional[sublime_plugin.CommandInputHandler]:
        if args.get("bmark_name") is None:
            help_view = find_help_view()
            if help_view is not None:
                return BookmarkNameInputHandler(help_view, self.bmark_type)

        return None


class BookmarkNameInputHandler(sublime_plugin.TextInputHandler):
    """
    Allow the user to select a name for their bookmark, showing a default name
    based on the current context and bookmark type.
    """
    def __init__(self, help_view: sublime.View, bmark_type: str) -> None:
        super().__init__()
        self.view = help_view
        self.bmark_type = bmark_type

    def name(self) -> str:
        return "bmark_name"

    def placeholder(self) -> str:
        return "bookmark name"

    def preview(self, text: str) -> str:
        return "The name for this bookmark"

    def initial_text(self) -> str:
        v = self.view

        link_info = None
        if len(v.sel()) > 0 and v.match_selector(v.sel()[0].b, "meta.link"):
            link_info = _get_link_topic(v, v.extract_scope(v.sel()[0].b))

        if self.bmark_type == "topic" and link_info is not None:
            pkg = link_info["pkg"]
            pkg_info = (help_index_list().get(pkg)
                        if pkg is not None else None)
            if pkg_info is not None:
                topic = lookup_help_topic(pkg_info, link_info["topic"])
                if topic is not None:
                    return topic["caption"]

        file = current_help_file()
        package = current_help_package()
        name = "File {} in help package {}".format(file, package)
        pkg_info = (help_index_list().get(package)
                    if package is not None else None)

        if pkg_info is not None and file is not None and file in pkg_info.help_files:
            name = pkg_info.help_files[file]

        if self.bmark_type == "view":
            name = name + " (view)"

        return name


###----------------------------------------------------------------------------
