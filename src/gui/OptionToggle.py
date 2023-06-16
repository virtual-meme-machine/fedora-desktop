import json
import os

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import data.OperationType as OperationType
import data.Category as Category

RESOURCES_DIR: str = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "resources"))


class OptionToggle:
    """
    Stores data for a single operation that the user can choose to preform or not
    """

    def __init__(self,
                 name: str,
                 description: str,
                 category: Category.Category,
                 operation_type: OperationType.OperationType,
                 operation_args: list):
        """
        Stores data for a single operation that the user can choose to preform or not
        :param name: Readable name for the option, eg: "Remove Firefox"
        :param description: Description for the option, eg: "Uninstalls Mozilla Firefox"
        :param category: Category the option should be grouped with, eg: Category.APPLICATION
        :param operation_type: Type of operation that will be preformed, eg: OperationType.PACKAGE_REMOVE
        :param operation_args: Arguments that should be passed to the operation, eg: ["firefox"]
        """
        self.name: str = name
        self.description: str = description
        self.category: Category.Category = category
        self.operation_type: OperationType.OperationType = operation_type
        self.operation_args: list = operation_args
        self.check_button = Gtk.CheckButton(active=True,
                                            halign=Gtk.Align.FILL,
                                            label=self.name,
                                            tooltip_text=self.description)

    def get_active(self) -> bool:
        """
        Checks the state of the option
        :return: True if check button is toggled on, False if not
        """
        return self.check_button.get_active()


def import_options() -> list[OptionToggle]:
    """
    Imports OptionToggle objects from JSON files in the resources directory
    :return: List of OptionToggle objects
    """
    options: list[OptionToggle] = []

    for option_file in os.listdir(RESOURCES_DIR):
        if not os.path.splitext(option_file)[1] == ".json":
            continue

        with open(os.path.join(RESOURCES_DIR, option_file), "r") as json_file:
            for option in json.load(json_file):
                options.append(OptionToggle(name=option.get("name"),
                                            description=option.get("description"),
                                            category=Category.from_string(option.get("category")),
                                            operation_type=OperationType.from_string(option.get("operation_type")),
                                            operation_args=option.get("operation_args")))

    return options
