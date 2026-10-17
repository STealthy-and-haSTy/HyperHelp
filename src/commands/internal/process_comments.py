import sublime
import sublime_plugin

from .common import _can_post_process


###----------------------------------------------------------------------------


class HyperhelpInternalProcessCommentsCommand(sublime_plugin.TextCommand):
    """
    Remove all hyperhelp comments from a newly loaded help file.

    All text scoped as a comment (including newlines) will be redacted from the
    file.
    """
    def run(self, edit):
        for region in reversed(self.view.find_by_selector("comment.block.help")):
            self.view.erase(edit, region)

    def is_enabled(self):
        return _can_post_process(self.view)


###----------------------------------------------------------------------------
