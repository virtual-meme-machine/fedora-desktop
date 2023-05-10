from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "ding@rastersoft.com"


def execute():
    """
    Adds icons to the desktop
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
