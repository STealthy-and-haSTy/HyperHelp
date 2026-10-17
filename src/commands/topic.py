import sublime
import sublime_plugin

from ...helpcore.common import log
from ...helpcore.common import current_help_package
from ...helpcore.core import show_help_topic


###----------------------------------------------------------------------------


class HyperhelpTopicCommand(sublime_plugin.ApplicationCommand):
    """
    Display the provided help topic inside the given package. If package is
    None, infer it from the currently active help view.
    """
    def run(self, package=None, topic="index.txt"):
        package = package or current_help_package()
        topic = topic or "index.txt"

        if package is None:
            return log("Cannot display topic '%s'; cannot determine package",
                topic, status=True)

        show_help_topic(package, topic, history=True)


###----------------------------------------------------------------------------
