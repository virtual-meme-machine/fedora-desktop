import dataclasses

import gi

from data.Action import Action

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import data.Category as Category
from utils.platform_utils import get_fedora_version


@dataclasses.dataclass
class Option:
    """
    Stores data for a single setup option
    :param name: Readable name for the option, eg: "Remove Firefox"
    :param description: Description for the option, eg: "Uninstalls Mozilla Firefox"
    :param default_state: Denotes the default state of the toggle, True/Enabled or False/Disabled
    :param can_toggle: Denotes if the option can be toggled by the user or not
    :param category: Category the option should be grouped with, eg: Category.APPLICATION
    :param actions: List of actions that will be preformed to complete this option
    """
    name: str
    description: str
    default_state: bool
    can_toggle: bool
    category: Category.Category
    actions: list[Action]

    def __post_init__(self):
        """
        Initializes a GTK check button for this Option
        :return: None
        """
        self.check_button = Gtk.CheckButton(active=self.default_state,
                                            halign=Gtk.Align.FILL,
                                            label=self.name,
                                            sensitive=self.can_toggle,
                                            tooltip_text=self.description)

    @classmethod
    def from_dict(cls, option_dict: dict):
        """
        Loads an Option from a provided dictionary
        :param option_dict: Dictionary containing serialized Action data
        :return: Loaded Option object
        """
        fedora_version: int = get_fedora_version()
        supported = fedora_version not in option_dict.get("unsupported_versions", [])

        return Option(name=option_dict.get("name"),
                      description=option_dict.get("description"),
                      default_state=supported and option_dict.get("default_state"),
                      can_toggle=supported,
                      category=Category.from_string(option_dict.get("category")),
                      actions=[Action.from_dict(action_dict=action_dict) for action_dict in option_dict.get("actions")])
