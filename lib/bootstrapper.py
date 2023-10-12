import sublime

import os
import re
import codecs
import textwrap
from zipfile import ZipFile

from threading import Thread

from os.path import join, dirname, normpath, relpath
from importlib import __import__ as do_import


### ---------------------------------------------------------------------------


# These name the bootstrap package that we use to give Sublime access to our
# resources and commands, and the base name of the file within that package
# that is responsible for loading the commands into Sublime when the package
# is loaded.
bootstrap_pkg = "HyperHelp"
bootloader = "bootstrap"


### ---------------------------------------------------------------------------


def log(msg, *args, dialog=False, error=False, **kwargs):
    """
    Generate a message to the console and optionally as either a message or
    error dialog. The message will be formatted and dedented before being
    displayed, and will be prefixed with its origin.
    """
    msg = textwrap.dedent(msg.format(*args, **kwargs)).strip()

    if error:
        print("hyperhelp error:")
        return sublime.error_message(msg)

    for line in msg.splitlines():
        print("hyperhelp: {msg}".format(msg=line))

    if dialog:
        sublime.message_dialog(msg)


def set_initial_topic(package, topic):
    """
    Set a setting in the active window that tells the bootstrapped package to
    open an initial help topic the next time the package loads.
    """
    settings = sublime.active_window().settings()
    settings.set("hyperhelp.initial_topic", "%s:%s" % (package, topic))


def display_topic(package, topic):
    """
    Invoke the appropriate command to display the given help topic. The topic
    is presumed to be from our own package. This uses a timeout so that it can
    be invoked from within the bootstrap code.
    """
    sublime.set_timeout(lambda: sublime.run_command("hyperhelp_topic", {
        "package": package,
        "topic": topic
    }))


### ---------------------------------------------------------------------------


class BootstrapThread(Thread):
    """
    Spawns a background thread that will create or update the hyperhelp
    bootstrap package.
    """
    def __init__(self):
        super().__init__()
        self.settings = sublime.load_settings("Preferences.sublime-settings")


    def enable_package(self, reenable_resources):
        """
        Enables the system bootstrap package (if it exists) by ensuring that
        it is not in the list of ignored packages and then restoring any
        resources that were unloaded back to the views that were using them.
        """
        ignored_packages = self.settings.get("ignored_packages", [])

        if bootstrap_pkg in ignored_packages:
            ignored_packages.remove(bootstrap_pkg)
            self.settings.set("ignored_packages", ignored_packages)

        # Enable resources after a short delay to ensure that Sublime has had a
        # change to re-index them.
        if reenable_resources:
            sublime.set_timeout_async(lambda: self.enable_resources())


    def disable_package(self):
        """
        Disables the system bootstrap package (if it exists) by ensuring that
        none of the resources that it provides are currently in use and then
        adding it to the list of ignored packages so that Sublime will unload
        it.
        """
        self.disable_resources()

        ignored_packages = self.settings.get("ignored_packages", [])
        if bootstrap_pkg not in ignored_packages:
            ignored_packages.append(bootstrap_pkg)
            self.settings.set("ignored_packages", ignored_packages)


    def enable_resources(self):
        """
        Enables all resources being provided by the system boostrap package by
        restoring the state that was saved when the resources were disabled.
        """
        for window in sublime.windows():
            for view in window.views():
                s = view.settings()
                old_syntax = s.get("_hh_boot_syntax", None)
                if old_syntax is not None:
                    s.set("syntax", old_syntax)
                    s.erase("_hh_boot_syntax")


    def disable_resources(self):
        """
        Disables all resources being provided by the system bootstrap package
        by saving the state of items that are using them and then reverting
        them to temporary defaults.
        """
        prefix = "Packages/{pkg}/".format(pkg=bootstrap_pkg)

        # TODO if the package also contains a custom color scheme, this should
        # also temporarily reset the color scheme back to defaults and then
        # restore them later.
        for window in sublime.windows():
            for view in window.views():
                s = view.settings()
                syntax = s.get("syntax")
                if syntax.startswith(prefix):
                    s.set("_hh_boot_syntax", syntax)
                    s.set("syntax", "Packages/Text/Plain text.tmLanguage")


    def create_boot_loader(self, stub_loader_name):
        """
        Given the name of a file containing a stub system bootstrap loader,
        return the body of a loader that contains the version number of the
        core dependency.
        """
        try:
            from hyperhelpcore import version as ver_info

            with codecs.open(stub_loader_name, 'r', 'utf-8') as file:
                content = file.read()

            return re.sub(r"^__core_version_tuple\s+=\s+\(.*\)$",
                           "__core_version_tuple = {version}".
                              format(version=str(ver_info())),
                          content,
                          count=1,
                          flags=re.MULTILINE)
        except:
            log("Bootstrap error: Unable to create bootloader")
            raise


    def create_bootstrap_package(self, package, res_path):
        """
        Perform the task of actually creating the system bootstrap package from
        files in the given resource folder into the provided package.
        """
        try:
            success = True
            boot_file = "{file}.py".format(file=bootloader)

            with ZipFile(package, 'w') as zFile:
                for (path, dirs, files) in os.walk(res_path):
                    rPath = relpath(path, res_path) if path != res_path else ""

                    for file in files:
                        real_file = join(res_path, path, file)
                        archive_file = join(rPath, file)

                        if archive_file.endswith(".sublime-ignored"):
                            archive_file = archive_file[:-len(".sublime-ignored")]

                        if archive_file == boot_file:
                            content = self.create_boot_loader(real_file)
                            zFile.writestr(archive_file, content)
                        else:
                            zFile.write(real_file, archive_file)

        except Exception as err:
            success = False
            log("Bootstrap error: {reason}", reason=str(err))
            if os.path.exists(package):
                os.remove(package)

        return success


    def run(self):
        """
        Creates or updates the system bootstrap package by packaging up the
        contents of the resource directory.
        """
        self.disable_package()

        res_path = normpath(join(dirname(__file__), bootstrap_pkg))
        package = join(sublime.installed_packages_path(), bootstrap_pkg +
                            ".sublime-package")

        prefix = os.path.commonprefix([res_path, package])
        log("Bootstraping {path} to {pkg}",
            path=res_path[len(prefix):],
            pkg=package[len(prefix):])

        pkg_existed = os.path.isfile(package)
        success = self.create_bootstrap_package(package, res_path)

        self.enable_package(success)

        if not success:
            return log(
                """
                An error was encountered while updating HyperHelp.

                Please check the console to see what went wrong.
                HyperHelp will not be available until the problem
                is resolved.
                """, error=True)

        if pkg_existed:
            set_initial_topic("HyperHelp", "latest_update")
            log(
                """
                HyperHelp has been updated!

                In order to complete the update, restart Sublime
                Text.
                """, dialog=True)
        else:
            # TODO: A restart should not be required here, but there are
            # currently bootstrap issues.
            set_initial_topic("HyperHelp", "help_on_help.txt")
            log(
                """
                HyperHelp has been installed!

                In order to complete the install, restart Sublime
                Text.
                """, dialog=True)


### ---------------------------------------------------------------------------