import gi

gi.require_version("Adw", "1")
from gi.repository import Adw
from gui.MainWindow import MainWindow


class AdwApp(Adw.Application):
    """
    Main application class
    """

    def __init__(self, **kwargs):
        """
        Main application class
        :param kwargs: Application arguments
        """
        super().__init__(**kwargs)
        self.win = None
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        """
        Loads the application window
        :param app: Gtk application window
        :return: None
        """
        self.win = MainWindow(application=app)
        self.win.present()
