import sublime
import sublime_plugin

import time

from .common import _can_post_process

from ....helpcore.core import parse_help_header
from ....helpcore.common import hh_setting
from ....helpcore.common import current_help_file


###----------------------------------------------------------------------------


class HyperhelpInternalProcessHeaderCommand(sublime_plugin.TextCommand):
    """
    Process the header in a newly loaded help file by finding and replacing the
    source level meta header with the fully expanded user-facing header.

    Nothing happens if the current file does not appear to have an appropriate
    meta-header line.
    """
    def run(self, edit):
        help_file = current_help_file(self.view)
        first_line = self.view.substr(self.view.full_line(0))

        header = parse_help_header(help_file, first_line)
        if header is None:
            return

        _hdr_width = 80
        _time_fmt = hh_setting("hyperhelp_date_format")

        file_target = "*%s*" % help_file
        title = header.title
        date_str = "Not Available"

        if header.date != 0:
            date_str = time.strftime(_time_fmt, time.localtime(header.date))

        # Take into account two extra spaces on either side of the title
        max_title_len = _hdr_width - len(file_target) - len(date_str) - 4
        if len(title) > max_title_len:
            title = title[:max_title_len-1] + '\u2026'

        header_line = "%s  %s  %s\n%s\n" % (
            file_target,
            "%s" % title.center(max_title_len, " "),
            date_str,
            ("=" * _hdr_width)
        )

        self.view.replace(edit, self.view.full_line(0), header_line)

    def is_enabled(self):
        return _can_post_process(self.view)


###----------------------------------------------------------------------------
