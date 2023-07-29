from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "ddterm@amezin.github.com"


def execute():
    """
    Provides a drop-down terminal on a hotkey press
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
