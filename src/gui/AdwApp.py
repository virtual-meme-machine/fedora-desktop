import gi
from gi.repository.Gio import ApplicationCommandLine

from data.Info import APPLICATION_AUTHOR, APPLICATION_ID, APPLICATION_NAME, get_application_version
from data.OptionStore import OptionStore
from utils.platform_utils import get_distro_full_name
from utils.print_utils import print_header
from workflows.setup import setup

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw
from gui.MainWindow import MainWindow
from gi.repository import Gio, GLib

PROFILE_ARG: str = "profile"


class AdwApp(Adw.Application):
    """
    Main application class
    """

    def __init__(self, *args, **kwargs):
        """
        Main application class
        :param kwargs: Application arguments
        """
        # Initialize application
        super().__init__(*args,
                         application_id=APPLICATION_ID,
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.win = None
        self.connect("activate", self.on_activate)

        # Initialize CLI args
        self.add_main_option(
            PROFILE_ARG,
            ord("p"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.FILENAME,
            "Profile file that should be loaded for non-interactive mode",
            "PROFILE_FILE",
        )

        # Print startup message
        print_header(f"{APPLICATION_NAME}\n"
                     f"Version {get_application_version()}\n"
                     f"(C) {APPLICATION_AUTHOR}")
        print(f"Host OS: {get_distro_full_name()}")

    def do_command_line(self, command_line: ApplicationCommandLine) -> int:
        """
        Determines if the application should run in GUI mode or CLI mode, then triggers the appropriate workflow
        :param command_line: Object for interfacing with command line via Gio
        :return: CLI workflow exit code
        """
        if not command_line.get_options_dict().contains(PROFILE_ARG):
            self.activate()
            return 0

        print(f"CLI args provided, starting setup in non-interactive mode")
        profile_file = bytes(command_line.get_options_dict().lookup_value(PROFILE_ARG).get_bytestring()).decode()
        option_store = OptionStore()
        if not option_store.profile_load(profile_file):
            exit(1)

        setup(option_store)
        return 0

    def on_activate(self, app):
        """
        Loads the application window
        :param app: Gtk application window
        :return: None
        """
        self.win = MainWindow(application=app)
        self.win.present()
