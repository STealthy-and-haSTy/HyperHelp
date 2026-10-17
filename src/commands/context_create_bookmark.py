import sublime
import sublime_plugin


###----------------------------------------------------------------------------


class HyperhelpContextCreateBookmarkCommand(sublime_plugin.TextCommand):
    def run(self, edit, event=None):
        if event is not None:
            point = self.view.window_to_text((event["x"], event["y"]))
            bmark_type = "file"
            if self.view.match_selector(point, "meta.link"):
                bmark_type = "topic"
                self.view.sel().clear()
                self.view.sel().add(sublime.Region(point))

            sublime.run_command("hyperhelp_prompt_create_bookmark", {
                "bmark_type": bmark_type})
        else:
            log("Cannot create a context sensitive bookmark without the mouse",
                status=True)

    def description(self, event=None):
        v = self.view
        if event is not None:
            point = v.window_to_text((event["x"], event["y"]))
            if v.match_selector(point, "meta.link"):
                return "HyperHelp: Bookmark this link"

        return "HyperHelp: Bookmark this file"

    def want_event(self):
        return True

    def is_enabled(self, event=None):
        return self.view.match_selector(0, "text.hyperhelp.help")

    def is_visible(self, event=None):
        return self.is_enabled(event)


###----------------------------------------------------------------------------
