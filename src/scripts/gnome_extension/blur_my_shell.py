from utils.dnf_utils import install_packages
from utils.gnome_extension_utils import enable_extension


def execute():
    """
    Blurs some elements of the Gnome Shell
    :return: None
    """
    install_packages(["gnome-shell-extension-blur-my-shell"])
    enable_extension("blur-my-shell@aunetx")
