import sublime
import sublime_plugin

import textwrap

from ...helpcore.common import log

from ...helpcore import __version__ as sys_version


###----------------------------------------------------------------------------


class HyperHelpAboutCommand(sublime_plugin.ApplicationCommand):
    """
    Displays a dialog box that indicates what the current version of HyperHelp
    and the core are, for diagnostic purposes.
    """
    def run(self):
        # Until the log code in the bootstrap and the log code in the core are
        # synchronized, manually do a dedent. I don't want to break anything
        # too close to the initial package announcement.
        msg = textwrap.dedent("""
            About HyperHelp

            HyperHelp Version: {sys}

            HyperHelp is a text based, hyper linked help system for
            Sublime Text that allows packages to display their
            help directly within Sublime.
        """).format(sys=sys_version).strip()
        log(msg, dialog=True)


###----------------------------------------------------------------------------
