import sublime

from ..helpcore.common import hh_setting, log


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


def post_install_update_check():
    """
    Check all windows to see if any of them are declaring that there should be
    an initial topic shown; if so, navigate to it after removing the setting.

    This is invoked on plugin load so that the event system for package control
    can indicate that the help package should display either its initial help
    page, or a changelog.

    As of right now, this integration is not yet complete, so this is still a
    TODO on that end; see [HH-3].
    """
    log('TODO: performing the post install update check')
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