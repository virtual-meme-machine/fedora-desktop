from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "ddterm@amezin.github.com"
def execute():
    """
    Provides a terminal hotkey
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
