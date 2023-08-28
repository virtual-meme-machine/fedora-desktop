import datetime
import getpass
import subprocess
import threading

import gi

from data.Category import from_string
from data.Info import APPLICATION_AUTHOR, APPLICATION_NAME, get_application_version
from data.OptionStore import OptionStore
from data.Paths import PROFILES_DIR
from utils.platform_utils import get_distro_full_name
from workflows.setup import setup

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GLib, Gtk

HEADER: list[str] = [
    f"Welcome to {get_distro_full_name()}!",
    f"This tool automatically installs software and configures settings.",
    f"Select the actions you wish to perform:"
]
WINDOW_MARGIN: int = 10
WINDOW_SIZE: (int, int) = (500, 800)

ABOUT_COPYRIGHT: str = f"Copyright {datetime.date.today().year}"
ABOUT_LICENSE: Gtk.License = Gtk.License.GPL_2_0
ABOUT_LOGO: str = "org.fedoraproject.AnacondaInstaller"
ABOUT_WEBSITE: str = "https://github.com/virtual-meme-machine/fedora-desktop"
ABOUT_WEBSITE_LABEL: str = "View source code on GitHub"
HELP_URL: str = "https://github.com/virtual-meme-machine/fedora-desktop/blob/main/README.md"


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
        print(f"Displaying option selection GUI")

        # Initialize window properties
        super().__init__(*args, **kwargs)
        self.set_default_size(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.set_resizable(False)
        self.set_title(APPLICATION_NAME)

        # Initialize application properties
        GLib.set_application_name(APPLICATION_NAME)

        # Initialize actions
        action_save_profile = Gio.SimpleAction.new("save_profile", None)
        action_save_profile.connect("activate", self.action_dialog_save_profile)
        self.add_action(action_save_profile)
        action_load_profile = Gio.SimpleAction.new("load_profile", None)
        action_load_profile.connect("activate", self.action_dialog_load_profile)
        self.add_action(action_load_profile)
        action_show_help = Gio.SimpleAction.new("show_help", None)
        action_show_help.connect("activate", self.action_show_help)
        self.add_action(action_show_help)
        action_show_about = Gio.SimpleAction.new("show_about", None)
        action_show_about.connect("activate", self.action_show_about)
        self.add_action(action_show_about)

        # Initialize application menu
        self.menu = Gio.Menu.new()
        profiles_section = Gio.Menu.new()
        profiles_section.append("Save Profile", "win.save_profile")
        profiles_section.append("Load Profile", "win.load_profile")
        self.menu.append_section(None, profiles_section)
        help_section = Gio.Menu.new()
        help_section.append("Help", "win.show_help")
        help_section.append("About", "win.show_about")
        self.menu.append_section(None, help_section)
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(self.menu)
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        # Initialize header bar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.header.pack_end(self.hamburger)

        # Initialize shortcuts
        self.get_application().set_accels_for_action("win.save_profile", ["<Control>s"])
        self.get_application().set_accels_for_action("win.load_profile", ["<Control>l"])
        self.get_application().set_accels_for_action("win.show_help", ["F1"])

        # Initialize OptionStore
        self.option_store: OptionStore = OptionStore()
        options = self.option_store.get_options()

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
        self.category_check_buttons = {}
        options_box = Gtk.Box(margin_top=WINDOW_MARGIN,
                              margin_bottom=WINDOW_MARGIN,
                              orientation=Gtk.Orientation.VERTICAL,
                              vexpand=True)
        for category in options.keys():
            expander_box = Gtk.Box(margin_start=40,
                                   orientation=Gtk.Orientation.VERTICAL)

            # Initialize category check button
            category_check_button = Gtk.CheckButton(halign=Gtk.Align.FILL,
                                                    label=category.value[1])
            category_check_button.connect("toggled", self.check_button_action_category_toggle)
            self.category_check_buttons.update({category: category_check_button})
            options_box.append(Gtk.Expander(child=expander_box,
                                            label_widget=category_check_button))

            # Initialize option check buttons
            for option in options.get(category):
                expander_box.append(option.check_button)
                option.check_button.connect("toggled", self.check_button_action_option_toggle)
        main_box.append(Gtk.ScrolledWindow(child=options_box))

        # Initialize select all and unselect all buttons
        select_buttons_box = Gtk.Box(margin_top=WINDOW_MARGIN,
                                     margin_bottom=WINDOW_MARGIN,
                                     orientation=Gtk.Orientation.HORIZONTAL,
                                     spacing=WINDOW_MARGIN)
        button_select_all = Gtk.Button(label="Select All")
        button_select_all.connect("clicked", self.button_action_select_all)
        select_buttons_box.append(button_select_all)
        button_unselect_all = Gtk.Button(label="Unselect All")
        button_unselect_all.connect("clicked", self.button_action_unselect_all)
        select_buttons_box.append(button_unselect_all)

        # Initialize selected count label
        self.selected_count = Gtk.Label()
        select_buttons_box.append(self.selected_count)
        main_box.append(select_buttons_box)
        main_box.append(Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL))

        # Initialize begin installation button
        self.button_begin_setup = Gtk.Button(label="Begin Setup", margin_top=WINDOW_MARGIN)
        self.button_begin_setup.connect("clicked", self.button_action_setup)
        main_box.append(self.button_begin_setup)

        # Run selection update method to sync button state with data
        self.check_button_action_option_toggle(None)

    def action_dialog_load_profile(self, action: Gio.SimpleAction, param: object):
        """
        Displays a dialog for selecting a profile to load
        :param action: Action that triggered this method
        :param param: Parameters passed into this method
        :return: None
        """
        profile_filter = Gtk.FileFilter()
        profile_filter.add_pattern("*.profile")

        file_chooser = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN,
                                             filter=profile_filter,
                                             modal=True,
                                             title="Select a profile to load",
                                             transient_for=self)
        file_chooser.add_button("Cancel", Gtk.ResponseType.CANCEL)
        file_chooser.add_button("Load", Gtk.ResponseType.ACCEPT)
        file_chooser.set_current_folder(Gio.File.new_for_path(PROFILES_DIR))
        file_chooser.set_default_response(Gtk.ResponseType.ACCEPT)
        file_chooser.connect("response", self.profile_load)
        file_chooser.show()

    def action_dialog_save_profile(self, action: Gio.SimpleAction, param: object):
        """
        Displays a dialog for saving the current profile to a file
        :param action: Action that triggered this method
        :param param: Parameters passed into this method
        :return: None
        """
        profile_filter = Gtk.FileFilter()
        profile_filter.add_pattern("*.profile")

        file_chooser = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.SAVE,
                                             create_folders=True,
                                             filter=profile_filter,
                                             modal=True,
                                             title="Save profile",
                                             transient_for=self)
        file_chooser.add_button("Cancel", Gtk.ResponseType.CANCEL)
        file_chooser.add_button("Save", Gtk.ResponseType.ACCEPT)
        file_chooser.set_current_folder(Gio.File.new_for_path(PROFILES_DIR))
        file_chooser.set_current_name(f"{getpass.getuser()}_default.profile")
        file_chooser.set_default_response(Gtk.ResponseType.ACCEPT)
        file_chooser.connect("response", self.profile_save)
        file_chooser.show()

    def action_show_about(self, action: Gio.SimpleAction, param: object):
        """
        Displays an about dialog
        :param action: Action that triggered this method
        :param param: Parameters passed into this method
        :return: None
        """
        about = Gtk.AboutDialog(authors=[APPLICATION_AUTHOR],
                                copyright=ABOUT_COPYRIGHT,
                                license_type=ABOUT_LICENSE,
                                logo_icon_name=ABOUT_LOGO,
                                modal=True,
                                title="About",
                                transient_for=self,
                                website=ABOUT_WEBSITE,
                                website_label=ABOUT_WEBSITE_LABEL,
                                version=get_application_version())
        about.show()

    def action_show_help(self, action: Gio.SimpleAction, param: object):
        """
        Opens help documentation in the browser
        :param action: Action that triggered this method
        :param param: Parameters passed into this method
        :return: None
        """
        subprocess.call(["/usr/bin/xdg-open", HELP_URL])

    def button_action_setup(self, button: Gtk.Button):
        """
        Triggers the setup workflow in another thread and closes this window
        Triggered by: 'Setup 'Button at the bottom of the window
        :param button: Button that triggered this method
        :return: None
        """
        install_thread = threading.Thread(target=setup, args=[self.option_store])
        install_thread.start()
        self.close()

    def button_action_select_all(self, button: Gtk.Button):
        """
        Selects all options
        Triggered by: 'Select All' Button at the bottom of the window
        :param button: Button that triggered this method
        :return: None
        """
        for option_list in self.option_store.get_options().values():
            for option in option_list:
                option.check_button.set_active(True)

    def button_action_unselect_all(self, button: Gtk.Button):
        """
        Unselects all options
        Triggered by: 'Unselect All' Button at the bottom of the window
        :param button: Button that triggered this method
        :return: None
        """
        for option_list in self.option_store.get_options().values():
            for option in option_list:
                option.check_button.set_active(False)

    def check_button_action_category_toggle(self, button: Gtk.CheckButton):
        """
        Selects or unselects all options in the button's category
        Triggered by: Category CheckButtons
        :param button: Button that triggered this method
        :return: None
        """
        category = from_string(button.get_label())
        state = button.get_active()
        for option in self.option_store.get_options().get(category):
            option.check_button.set_active(state)

    def check_button_action_option_toggle(self, button: Gtk.Button or None):
        """
        - Updates the label that counts how many options have been selected
        - Enables or disables the 'Begin Setup' button if there are options selected or not
        - Toggles Category CheckButtons if all category options are set to the same value
        Triggered by: Option CheckButtons
        :param button: Button that triggered this method
        :return: None
        """
        self.selected_count.set_label(self.option_store.get_selected_string())

        if self.option_store.get_selected_count() == 0:
            self.button_begin_setup.set_sensitive(False)
        elif not self.button_begin_setup.get_sensitive():
            self.button_begin_setup.set_sensitive(True)

        options = self.option_store.get_options()
        for category in options.keys():
            if all(option.check_button.get_active() is True for option in options.get(category)):
                self.category_check_buttons.get(category).set_active(True)
            elif all(option.check_button.get_active() is False for option in options.get(category)):
                self.category_check_buttons.get(category).set_active(False)

    def profile_load(self, dialog: Gtk.FileChooserDialog, response: Gtk.ResponseType):
        """
        Loads a profile from file
        :param dialog: Dialog window that triggered this method
        :param response: Response returned by the dialog
        :return: None
        """
        dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
            return
        elif response == Gtk.ResponseType.ACCEPT:
            self.option_store.profile_load(dialog.get_file().get_path())

    def profile_save(self, dialog: Gtk.FileChooserDialog, response: Gtk.ResponseType):
        """
        Saves a profile to file
        :param dialog: Dialog window that triggered this method
        :param response: Response returned by the dialog
        :return: None
        """
        dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
            return
        elif response == Gtk.ResponseType.ACCEPT:
            self.option_store.profile_save(dialog.get_file().get_path())
