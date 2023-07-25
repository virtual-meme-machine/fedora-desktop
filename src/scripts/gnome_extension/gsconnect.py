from utils.dnf_utils import install_packages
from utils.gnome_extension_utils import enable_extension


def execute():
    """
    Mobile device bridge that integrates device notifications, messages, and more into Gnome Shell
    :return: None
    """
    install_packages(["gnome-shell-extension-gsconnect", "nautilus-gsconnect", "webextension-gsconnect"])
    enable_extension("gsconnect@andyholmes.github.io")
