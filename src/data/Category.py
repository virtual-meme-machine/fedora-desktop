from enum import Enum


class Category(Enum):
    """
    Option category, used to group options in the GUI
    """
    APPLICATION: str = "application", "Install Applications"
    EMULATOR: str = "emulator", "Install Emulators"
    GAME: str = "game", "Install Games"
    GNOME_EXTENSION: str = "gnome_extension", "Install Gnome Shell Extensions"
    SETTING: str = "setting", "Configure Settings"
    SYSTEM: str = "system", "Configure System"
    VPN: str = "vpn", "Configure VPN"


def from_string(string: str) -> Category:
    """
    Gets a Category from the provided input
    :param string: String that we want to get a Category value for
    :return: Corresponding Category value
    """
    for category in Category:
        for value in category.value:
            if value == string:
                return category

    raise ValueError(f"Invalid Category: '{string}'")
