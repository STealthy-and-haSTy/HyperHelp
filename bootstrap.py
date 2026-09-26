import sublime

from .helpcore.common import hh_setting


### ---------------------------------------------------------------------------


def display_topic(package, topic):
    """
    Invoke the appropriate command to display the given help topic. The topic
    is presumed to be from our own package. This uses a timeout because it used
    to be invoked from within the bootstrap code. Probably no longer need
    though.
    """
    sublime.set_timeout(lambda: sublime.run_command("hyperhelp_topic", {
        "package": package,
        "topic": topic
    }))


### ---------------------------------------------------------------------------


def plugin_loaded():
    """
    On plugin load, see if we should display an initial help topic or not.
    This relies on a window setting that the bootstrapper applies to whatever
    the current window is, and will display an appropriate topic based on what
    the bootstrap did.
    """
    topic = None
    for window in sublime.windows():
        settings = window.settings()
        if settings.has("hyperhelp.initial_topic"):
            topic = topic or settings.get("hyperhelp.initial_topic")
            settings.erase("hyperhelp.initial_topic")

    if topic is not None and hh_setting("show_changelog"):
        package, topic = topic.split(":")
        display_topic(package, topic)


### ---------------------------------------------------------------------------