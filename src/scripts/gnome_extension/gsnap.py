from utils.gnome_extension_utils import enable_extension, install_remote_extension

ID: str = "gSnap@micahosborne"


def execute():
    """
    Organize windows in customizable snap zones like FancyZones on Windows.
    :return: None
    """
    install_remote_extension(ID)
    enable_extension(ID)
