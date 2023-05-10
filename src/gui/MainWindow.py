import datetime
import threading

import gi

from data.Category import Category
from gui.OptionToggle import OptionToggle, import_options
from utils.platform_utils import get_distro_full_name, get_script_version
from utils.print_utils import print_header
from workflows.setup import setup

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GLib, Gtk

APPLICATION_NAME: str = "Fedora Desktop Configurator"
HEADER: list[str] = [
    f"Welcome to {get_distro_full_name()}!",
    f"This tool automatically installs software and configures settings.",
    f"Select the actions you wish to preform:"
]
WINDOW_MARGIN: int = 10
WINDOW_SIZE: (int, int) = (500, 800)

ABOUT_AUTHOR: str = "virtual-meme-machine"
ABOUT_BUTTON_LABEL: str = f"About {APPLICATION_NAME}"
ABOUT_COPYRIGHT: str = f"Copyright {datetime.date.today().year}"
ABOUT_LICENSE: Gtk.License = Gtk.License.GPL_2_0
ABOUT_LOGO: str = "org.fedoraproject.AnacondaInstaller"
ABOUT_WEBSITE: str = "https://github.com/virtual-meme-machine/fedora-desktop"
ABOUT_WEBSITE_LABEL: str = "View source code on GitHub"
ABOUT_VERSION: str = get_script_version()


class MainWindow(Gtk.ApplicationWindow):
    """
    Main application window
    """

    def __init__(self, *args, **kwargs):
        """
        Main application window
        :param args: Arguments
        :param kwargs: Keyword arguments
        """
        # Print startup message
        print_header(f"{APPLICATION_NAME}\n"
                     f"Version {get_script_version()}\n"
                     f"(C) {ABOUT_AUTHOR}")
        print(f"Host OS: {get_distro_full_name()}")
        print(f"Displaying option selection GUI")

        # Initialize window properties
        super().__init__(*args, **kwargs)
        self.set_default_size(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.set_resizable(False)
        self.set_title(APPLICATION_NAME)

        # Initialize application properties
        GLib.set_application_name(APPLICATION_NAME)

        # Initialize application menu
        self.menu = Gio.Menu.new()
        self.menu.append(ABOUT_BUTTON_LABEL, "win.about")
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(self.menu)
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        # Initialize header bar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.header.pack_end(self.hamburger)

        # Initialize actions
        action_show_about = Gio.SimpleAction.new("about", None)
        action_show_about.connect("activate", self.menu_show_about)
        self.add_action(action_show_about)

        # Initialize option list
        self.option_list: list[OptionToggle] = sorted(import_options(), key=lambda o: o.name.lower())

        # Initialize main window box and header labels
        main_box = Gtk.Box(margin_top=WINDOW_MARGIN,
                           margin_bottom=WINDOW_MARGIN,
                           margin_start=WINDOW_MARGIN,
                           margin_end=WINDOW_MARGIN,
                           orientation=Gtk.Orientation.VERTICAL)
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                             spacing=WINDOW_MARGIN)
        for line in HEADER:
            header_box.append(Gtk.Label(label=line))
        header_box.append(Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL))
        main_box.append(header_box)
        self.set_child(main_box)

        # Initialize expander sections for each option category
        options_box = Gtk.Box(margin_top=WINDOW_MARGIN,
                              margin_bottom=WINDOW_MARGIN,
                              orientation=Gtk.Orientation.VERTICAL,
                              spacing=WINDOW_MARGIN,
                              vexpand=True)
        for category in Category:
            expander_box = Gtk.Box(margin_start=WINDOW_MARGIN,
                                   margin_top=WINDOW_MARGIN,
                                   orientation=Gtk.Orientation.VERTICAL)
            options_box.append(Gtk.Expander(child=expander_box,
                                            label=category.value[1]))
            for option in self.option_list:
                if option.category == category:
                    expander_box.append(option.check_button)
        main_box.append(Gtk.ScrolledWindow(child=options_box))

        # Initialize select / deselect all buttons
        select_buttons_box = Gtk.Box(margin_top=WINDOW_MARGIN,
                                     margin_bottom=WINDOW_MARGIN,
                                     orientation=Gtk.Orientation.HORIZONTAL,
                                     spacing=WINDOW_MARGIN)
        button_select_all = Gtk.Button(label="Select All")
        button_select_all.connect("clicked", self.button_action_select_all)
        select_buttons_box.append(button_select_all)
        button_deselect_all = Gtk.Button(label="Deselect All")
        button_deselect_all.connect("clicked", self.button_action_deselect_all)
        select_buttons_box.append(button_deselect_all)
        main_box.append(select_buttons_box)
        main_box.append(Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL))

        # Initialize begin installation button
        button_begin_setup = Gtk.Button(label="Begin Setup", margin_top=WINDOW_MARGIN)
        button_begin_setup.connect("clicked", self.button_action_setup)
        main_box.append(button_begin_setup)

    def button_action_setup(self, button: Gtk.Button):
        """
        Triggers the setup workflow in another thread and closes this window
        :param button: Button that triggered this method
        :return: None
        """
        install_thread = threading.Thread(target=setup, args=[self.option_list])
        install_thread.start()
        self.close()

    def button_action_select_all(self, button: Gtk.Button):
        """
        Selects all options
        :param button: Button that triggered this method
        :return: None
        """
        for option in self.option_list:
            option.check_button.set_active(True)

    def button_action_deselect_all(self, button: Gtk.Button):
        """
        Deselects all options
        :param button: Button that triggered this method
        :return: None
        """
        for option in self.option_list:
            option.check_button.set_active(False)

    def menu_show_about(self, action: Gio.SimpleAction, param: object):
        """
        Displays an about dialog
        :param action: Action that triggered this method
        :param param: Parameters passed into this method
        :return: None
        """
        about = Gtk.AboutDialog()
        about.set_transient_for(self)
        about.set_modal(True)
        about.set_authors([ABOUT_AUTHOR])
        about.set_copyright(ABOUT_COPYRIGHT)
        about.set_license_type(ABOUT_LICENSE)
        about.set_logo_icon_name(ABOUT_LOGO)
        about.set_website(ABOUT_WEBSITE)
        about.set_website_label(ABOUT_WEBSITE_LABEL)
        about.set_version(ABOUT_VERSION)
        about.show()
