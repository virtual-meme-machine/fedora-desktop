from utils.gnome_extension_utils import enable_extension, install_remote_extension
from utils.platform_utils import set_dconf_values

ID: str = "AlphabeticalAppGrid@stuarthayhurst"
SETTINGS: list[dict] = [
    {
        "key": "/org/gnome/shell/extensions/alphabetical-app-grid/folder-order-position",
        "value": "'start'"
    }
]


def execute():
    """
    Automatically alphabetizes applications in the app picker
    :return: None
    """
    install_remote_extension(ID)
    set_dconf_values(SETTINGS)
    enable_extension(ID)
