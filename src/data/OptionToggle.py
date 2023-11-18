import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import data.OperationType as OperationType
import data.Category as Category


class OptionToggle:
    """
    Stores data for a single operation that the user can choose to perform or not
    """

    def __init__(self,
                 name: str,
                 description: str,
                 default_state: bool,
                 can_toggle: bool,
                 category: Category.Category,
                 operation_type: OperationType.OperationType,
                 operation_args: list):
        """
        Stores data for a single operation that the user can choose to perform or not
        :param name: Readable name for the option, eg: "Remove Firefox"
        :param description: Description for the option, eg: "Uninstalls Mozilla Firefox"
        :param default_state: Denotes the default state of the toggle, True/Enabled or False/Disabled
        :param can_toggle: Denotes if the option can be toggled by the user or not
        :param category: Category the option should be grouped with, eg: Category.APPLICATION
        :param operation_type: Type of operation that will be performed, eg: OperationType.PACKAGE_REMOVE
        :param operation_args: Arguments that should be passed to the operation, eg: ["firefox"]
        """
        self.name: str = name
        self.description: str = description
        self.default_state: bool = default_state
        self.can_toggle: bool = can_toggle
        self.category: Category.Category = category
        self.operation_type: OperationType.OperationType = operation_type
        self.operation_args: list = operation_args
        self.check_button = Gtk.CheckButton(active=default_state,
                                            halign=Gtk.Align.FILL,
                                            label=self.name,
                                            sensitive=self.can_toggle,
                                            tooltip_text=self.description)
