import sublime
import sublime_plugin

from ...helpcore.view import find_help_view
from ...helpcore.core import help_index_list
from ...helpcore.core import navigate_help_history, jump_help_history
from ...helpcore.core import clear_help_history
from ...helpcore.help import HistoryData


###----------------------------------------------------------------------------


class HyperhelpHistoryCommand(sublime_plugin.WindowCommand):
    """
    This command is for working with history in HyperHelp help views in a
    myriad of interesting ways.
    """
    available_actions = ["next", "prev", "jump", "clear"]

    def run(self, action, index=-1):
        if action in ["next", "prev"]:
            navigate_help_history(find_help_view(),
                                  True if action == "prev" else False)
        elif action == "clear":
            clear_help_history(find_help_view())

        else:
            self.show_history(index)

    def get_history_info(self, help_view=None):
        help_view = help_view or find_help_view()

        if help_view is not None:
            settings = help_view.settings()
            return (
                settings.get("_hh_hist_pos"),
                settings.get("_hh_hist")
            )

        return (None, None)

    def is_enabled(self, action, index=-1):
        help_view = find_help_view()
        if help_view is None or action not in self.available_actions:
            return False

        h_pos, h_info = self.get_history_info(help_view)
        h_len = len(h_info)

        if action in ["next", "prev"]:
            prev = True if action == "prev" else False
            if (prev and h_pos == 0) or (not prev and h_pos == h_len - 1):
                return False

        if action in ["clear", "jump"] and h_len == 1:
            return False

        return True

    def description(self, action, index=-1):
        # Docs say to return None, but that makes Sublime log an error.
        if action not in ["next", "prev"]:
            return ""

        prev = True if action == "prev" else False

        template = "Back" if prev else "Forward"
        h_pos, h_info = self.get_history_info()
        if h_pos is None:
            return template

        if (prev and h_pos == 0) or (not prev and h_pos == len(h_info) - 1):
            return template

        entry = HistoryData._make(h_info[h_pos + (-1 if prev else 1)])
        title = entry.file

        pkg_info = help_index_list().get(entry.package)
        if pkg_info is not None and entry.file in pkg_info.help_files:
            title = pkg_info.help_files[entry.file]

        return "%s: %s" % (template, title)

    def show_history(self, index):
        h_pos, h_info = self.get_history_info()

        if index >= 0 and index < len(h_info):
            return self.jump_to_entry(index)

        items = []
        for idx, info in enumerate(h_info):
            entry = HistoryData._make(info)

            pkg_info = help_index_list().get(entry.package)
            if pkg_info is not None and entry.file in pkg_info.help_files:
                title = pkg_info.help_files[entry.file]
                description = "%s in %s" % (entry.file, pkg_info.description)
            else:
                title = "%s in %s" % (entry.file, entry.package)
                description = ""

            if idx == h_pos:
                title = title + "\t\t[currently viewing]"

            items.append([title, description])

        self.window.show_quick_panel(items,
                                     lambda idx: self.jump_to_entry(idx),
                                     selected_index=h_pos)

    def jump_to_entry(self, entry_index):
        h_pos, h_info = self.get_history_info()

        if entry_index >= 0:
            jump_help_history(None, entry_index)


###----------------------------------------------------------------------------
