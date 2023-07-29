from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "noannoyance-fork@vrba.dev"


def execute():
    """
    Removes the 'window is ready' notification and puts the window into focus instead
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
