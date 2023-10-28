from utils.dnf_utils import install_packages
from utils.gnome_extension_utils import enable_extension

ID: str = "dash-to-panel@jderose9.github.com"


def execute():
    """
    An icon taskbar for the Gnome Shell
    :return: None
    """
    install_packages(["gnome-shell-extension-dash-to-panel"])
    enable_extension("dash-to-panel@jderose9.github.com")
