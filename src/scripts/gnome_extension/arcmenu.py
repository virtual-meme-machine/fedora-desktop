from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "arcmenu@arcmenu.com"


def execute():
    """
    Application menu for GNOME Shell
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
