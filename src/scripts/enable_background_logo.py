from utils.dnf_utils import install_packages
from utils.gnome_extension_utils import enable_extension
from utils.platform_utils import set_gsettings_values

LOGO_SETTINGS: list[dict] = [
    {
        "schema": "org.fedorahosted.background-logo-extension",
        "key": "logo-always-visible",
        "value": "true"
    },
    {
        "schema": "org.fedorahosted.background-logo-extension",
        "key": "logo-border",
        "value": "25"
    },
    {
        "schema": "org.fedorahosted.background-logo-extension",
        "key": "logo-opacity",
        "value": "20"
    },
    {
        "schema": "org.fedorahosted.background-logo-extension",
        "key": "logo-position",
        "value": "'bottom-right'"
    },
    {
        "schema": "org.fedorahosted.background-logo-extension",
        "key": "logo-size",
        "value": "5.0"
    }
]


def execute():
    """
    Adds a Fedora logo watermark to the wallpaper
    :return: None
    """
    install_packages(["gnome-shell-extension-background-logo"])
    enable_extension("background-logo@fedorahosted.org")
    set_gsettings_values(LOGO_SETTINGS)
