import sublime
import sublime_plugin

from ...helpcore.common import current_help_package
from ...helpcore.core import help_index_list


###----------------------------------------------------------------------------


class HyperhelpCurrentHelpCommand(sublime_plugin.WindowCommand):
    """
    This command does nothing, but it's description method tells you what
    help package is currently being browsed, if any.
    """
    def is_enabled(self, **kwargs):
        return False

    def description(self, no_help_fmt="No help currently visible",
                          help_fmt="Viewing help for: '%s'"):
        package = current_help_package(window=self.window)
        if package is None:
            return no_help_fmt

        pkg_info = help_index_list().get(package)
        package = package if pkg_info is None else pkg_info.description
        return help_fmt % package


###----------------------------------------------------------------------------
