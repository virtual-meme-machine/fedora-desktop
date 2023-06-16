from utils.dnf_utils import install_packages
from utils.flatpak_utils import install_flatpaks


def execute():
    """
    Installs OpenRGB
    :return: None
    """
    install_packages(["openrgb-udev-rules"])
    install_flatpaks(["org.openrgb.OpenRGB"])
    