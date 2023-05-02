import utils.dnf_utils as dnf_utils
import utils.flatpak_utils as flatpak_utils


def execute():
    """
    Installs any available updates
    :return: None
    """
    dnf_utils.install_updates()
    dnf_utils.auto_remove_packages()
    flatpak_utils.install_updates()
