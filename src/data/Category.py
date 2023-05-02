from enum import Enum


class Category(Enum):
    """
    Option category, used to group options in the GUI
    """
    APPLICATION: str = "application", "Applications"
    EMULATOR: str = "emulator", "Emulators"
    GAME: str = "game", "Games"
    GNOME_EXTENSION: str = "gnome_extension", "Gnome Shell Extensions"
    SETTING: str = "setting", "Settings"
    SYSTEM: str = "system", "System"


def from_string(string: str) -> Category:
    """
    Gets a Category from the provided input
    :param string: String that we want to get a Category value for
    :return: Corresponding Category value
    """
    for category in Category:
        if category.value[0] == string:
            return category

    raise ValueError(f"Invalid Category: '{string}'")
