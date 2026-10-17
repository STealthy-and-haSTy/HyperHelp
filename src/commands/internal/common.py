import sublime
import sublime_plugin


###----------------------------------------------------------------------------


def _can_post_process(view):
    """
    Determine if the provided view is eligible for a post processing command to
    execute within it or not.
    """
    return (view.match_selector(0, "text.hyperhelp.help") and
            view.settings().get("_hh_post_processing", False))


###----------------------------------------------------------------------------
