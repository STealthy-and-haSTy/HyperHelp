import sublime
import sublime_plugin


###----------------------------------------------------------------------------


class HyperhelpFocusCommand(sublime_plugin.TextCommand):
    """
    Alter the selection in the given view (which should be a help view but
    doesn't need to be) by clearing it and setting the single selection to the
    provided position and focusing that position in the view.

    The position of the focused text is adjusted in the window to be either  at
    the top, at the center, or just made visible, depending on the arguments.

    If at_top is true, it's used to set the position. Otherwise the text will
    be either centered or just visible based on the value of at_center.

    Position may be a single integer or a region.
    """
    def run(self, edit, position, at_top=False, at_center=False):
        if isinstance(position, int):
            position = sublime.Region(position)
        elif isinstance(position, list):
            position = sublime.Region(position[0], position[1])

        if at_top:
            offs = self.view.rowcol(position.begin())[0] * self.view.line_height()
            self.view.set_viewport_position((0.0, offs), True)
        elif at_center:
            self.view.show_at_center(position)
        else:
            self.view.show(position, True)

        self.view.sel().clear()
        self.view.sel().add(position)


###----------------------------------------------------------------------------
