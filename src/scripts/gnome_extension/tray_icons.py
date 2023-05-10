from utils.dnf_utils import install_packages
from utils.gnome_extension_utils import enable_extension


def execute():
    """
    Enables support for tray icons
    :return: None
    """
    install_packages(["gnome-shell-extension-appindicator"])
    enable_extension("appindicatorsupport@rgcjonas.gmail.com")
