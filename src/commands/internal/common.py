from __future__ import annotations

from typing import cast

import sublime         # noqa: F401
import sublime_plugin  # noqa: F401


###----------------------------------------------------------------------------


def _can_post_process(view: sublime.View) -> bool:
    """
    Determine if the provided view is eligible for a post processing command to
    execute within it or not.
    """
    return (view.match_selector(0, "text.hyperhelp.help") and
            cast(bool, view.settings().get("_hh_post_processing", False)))


###----------------------------------------------------------------------------
