from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "dash-to-panel@jderose9.github.com"


def execute():
    """
    An icon taskbar for the Gnome Shell
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
