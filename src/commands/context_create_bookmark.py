from __future__ import annotations

from typing import Any, Dict, Optional

import sublime
import sublime_plugin

from ...helpcore.common import log


###----------------------------------------------------------------------------


class HyperhelpContextCreateBookmarkCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit,
            event: Optional[Dict[str, Any]] = None) -> None:
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

    def description(self, event: Optional[Dict[str, Any]] = None) -> str:
        v = self.view
        if event is not None:
            point = v.window_to_text((event["x"], event["y"]))
            if v.match_selector(point, "meta.link"):
                return "HyperHelp: Bookmark this link"

        return "HyperHelp: Bookmark this file"

    def want_event(self) -> bool:
        return True

    def is_enabled(self, event: Optional[Dict[str, Any]] = None) -> bool:
        return self.view.match_selector(0, "text.hyperhelp.help")

    def is_visible(self, event: Optional[Dict[str, Any]] = None) -> bool:
        return self.is_enabled(event)


###----------------------------------------------------------------------------
