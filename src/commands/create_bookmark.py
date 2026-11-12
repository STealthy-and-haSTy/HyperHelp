from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import sublime  # noqa: F401
import sublime_plugin

from .common import _add_bookmark


###----------------------------------------------------------------------------


class HyperhelpCreateBookmarkCommand(sublime_plugin.ApplicationCommand):
    """
    Does the work of actually creating a bookmark using the given information,
    which is assumed to be correct and is not validated prior to generating the
    new bookmark entry.
    """
    def run(self, name: str, package: Optional[str], topic: Optional[str],
            caret: Optional[Tuple[int, int]] = None,
            viewport: Optional[Tuple[float, float]] = None) -> None:
        bookmark: Dict[str, Any] = {
            "name": name,
            "package": package,
            "topic": topic
        }

        if caret is not None:
            bookmark["caret"] = caret

            if viewport is not None:
                bookmark["viewport"] = viewport

        _add_bookmark(bookmark)


###----------------------------------------------------------------------------
