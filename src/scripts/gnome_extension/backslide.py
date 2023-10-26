from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "backslide@codeisland.org"


def execute():
    """
    Automatic background-image (wallpaper) slideshow for Gnome Shell.
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
