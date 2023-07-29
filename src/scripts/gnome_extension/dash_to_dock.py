from utils.dnf_utils import install_packages
from utils.gnome_extension_utils import enable_extension


def execute():
    """
    Moves the dash out of the overview transforming it into a dock
    :return: None
    """
    install_packages(["gnome-shell-extension-dash-to-dock"])
    enable_extension("dash-to-dock@micxgx.gmail.com")
