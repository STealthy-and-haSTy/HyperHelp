from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, cast

import sublime

import os
import codecs

from .data import HelpData
from .view import find_help_view


###----------------------------------------------------------------------------


_hh_settings: Optional[sublime.Settings] = None
_hh_setting_defaults: Dict[str, Any] = {
    "hyperhelp_date_format": "%x",
    "show_changelog": True,
    "focus_links_at_top": True,
    "bookmarks": []
}


def log(message: str, *args: object, status: bool = False,
        dialog: bool = False) -> None:
    """
    Log the provided message to the console, optionally also sending it to the
    status bar and a dialog box.
    """
    message = message % args
    for line in message.splitlines():
        print("HyperHelp:", line)
    if status:
        sublime.status_message(message)
    if dialog:
        sublime.message_dialog(message)


def hh_syntax(base_file: str) -> Optional[str]:
    """
    Return the syntax file associated with the given base syntax file name.
    This can return None if the syntax is not known.
    """
    syn_list = sublime.find_resources(base_file)
    if len(syn_list) == 1:
        return syn_list[0]

    log("Unable to locate unique syntax '%s'", base_file)
    return None


def hh_setting(key: str) -> Any:
    """
    Get a HyperHelp setting from a cached settings object.
    """
    global _hh_settings

    if _hh_settings is None:
        _hh_settings = sublime.load_settings("HyperHelp.sublime-settings")

    default = _hh_setting_defaults.get(key, None)
    return _hh_settings.get(key, default)


def hh_update_setting(key: str, value: Any, save: bool = False) -> None:
    """
    Set the value of a HyperHelp setting to the value provided. Optionally, the
    call can also persist the change to disk.
    """
    global _hh_settings

    if _hh_settings is None:
        _hh_settings = sublime.load_settings("HyperHelp.sublime-settings")

    _hh_settings.set(key, value)
    if save:
        sublime.save_settings("HyperHelp.sublime-settings")


def load_resource(res_name: str) -> Optional[str]:
    """
    Attempt to load and decode the UTF-8 encoded string with normalized line
    endings, returning the string on success or None on error.

    If no resource can be found with the resource specification provided, the
    call tries to load a file by this name from the packages folder instead.
    """
    try:
        text = sublime.load_binary_resource(res_name).decode("utf-8")
        return text.replace('\r\n', '\n').replace('\r', '\n')

    except OSError:
        pass

    except UnicodeError:
        log("Unable to decode '%s'; resource is not UTF-8", res_name)
        return None

    try:
        spp = os.path.split(sublime.packages_path())[0]
        file_name = os.path.join(spp, res_name)

        with codecs.open(file_name, 'r', 'utf-8') as file:
            return file.read().replace('\r\n', '\n').replace('\r', '\n')

    except OSError:
        log("Unable to load '%s'; resource not found", res_name)
        return None

    except UnicodeError:
        log("Unable to decode '%s'; resource is not UTF-8", res_name)
        return None


def current_help_package(view: Optional[sublime.View] = None,
                         window: Optional[sublime.Window] = None) -> Optional[str]:
    """
    Obtain the package that contains the currently displayed help file or None
    if help is not visible.

    Looks in the help view provided, or the help view in the passed in window,
    or the help view in the currently active window.
    """
    view = view or find_help_view(window)
    if view is None:
        return None

    return cast(Optional[str], view.settings().get("_hh_pkg"))


def current_help_file(view: Optional[sublime.View] = None,
                      window: Optional[sublime.Window] = None) -> Optional[str]:
    """
    Obtain the file that is currently being displayed in the help view or None
    if help is not visible.

    Looks in the help view provided, or the help view in the passed in window,
    or the help view in the currently active window.
    """
    view = view or find_help_view(window)
    if view is None:
        return None

    return cast(Optional[str], view.settings().get("_hh_file"))


def help_package_prompt(help_list: Dict[str, HelpData],
                        on_select: Callable[[str], Any],
                        on_cancel: Optional[Callable[[], Any]] = None) -> None:
    """
    Given a list of loaded help indexes, prompt the user to select one of the
    packages. on_select is invoked with the name of the selected package,
    while on_cancel is invoked if the user cancels the selection.
    """
    if not help_list:
        log("No packages with help are installed", status=True)
        return

    pkg_list = sorted([key for key in help_list])
    captions: List[List[str]] = [[help_list[key].package,
                                  help_list[key].description]
                                 for key in pkg_list]

    def pick_package(index: int) -> None:
        if index >= 0:
            on_select(captions[index][0])
        elif on_cancel is not None:
            on_cancel()

    sublime.active_window().show_quick_panel(
        captions,
        on_select=lambda index: pick_package(index))


###----------------------------------------------------------------------------
