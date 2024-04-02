from utils.gnome_extension_utils import enable_extension, install_remote_extension
from utils.platform_utils import set_dconf_values

ID: str = "quick-settings-audio-panel@rayzeq.github.io"
SETTINGS: list[dict] = [
    {
        "key": "/org/gnome/shell/extensions/quick-settings-audio-panel/always-show-input-slider",
        "value": "true"
    },
    {
        "key": "/org/gnome/shell/extensions/quick-settings-audio-panel/media-control",
        "value": "'none'"
    },
    {
        "key": "/org/gnome/shell/extensions/quick-settings-audio-panel/merge-panel",
        "value": "true"
    },
    {
        "key": "/org/gnome/shell/extensions/quick-settings-audio-panel/panel-position",
        "value": "'top'"
    }
]


def execute():
    """
    Adds extra volume controls to the quick settings menu
    :return: None
    """
    install_remote_extension(ID)
    set_dconf_values(SETTINGS)
    enable_extension(ID)
