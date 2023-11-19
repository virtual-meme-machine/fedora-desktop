import json
import os

import data.Category as Category
import data.OperationType as OperationType
from data.OptionToggle import OptionToggle
from data.Paths import OPTIONS_DIR
from utils.platform_utils import get_fedora_version


class OptionStore:
    """
    Stores and manages a set of OptionToggles
    """

    def __init__(self, options_dir: str = OPTIONS_DIR):
        """
        Stores and manages a set of OptionToggles
        :param options_dir: Directory containing serialized OptionToggle data
        :return: OptionStore object
        """
        self.__option_count: int = 0
        self.__options_dict: dict[Category, list[OptionToggle]] = {}

        temp_dict: dict[Category, list[OptionToggle]] = {}
        fedora_version: int = get_fedora_version()
        for option_file in os.listdir(options_dir):
            if not os.path.splitext(option_file)[1] == ".json":
                continue

            with open(os.path.join(options_dir, option_file), "r") as json_file:
                for option in json.load(json_file):
                    supported = fedora_version not in option.get("unsupported_versions", [])
                    option_toggle = OptionToggle(name=option.get("name"),
                                                 description=option.get("description"),
                                                 default_state=supported and option.get("default_state"),
                                                 can_toggle=supported,
                                                 category=Category.from_string(option.get("category")),
                                                 operation_type=OperationType.from_string(option.get("operation_type")),
                                                 operation_args=option.get("operation_args"))
                    key = option_toggle.category
                    sub_options = ([], temp_dict.get(key))[key in temp_dict.keys()]
                    sub_options.append(option_toggle)
                    temp_dict.update({key: sub_options})
                    self.__option_count += 1

        for key in sorted(temp_dict.keys(), key=lambda category: category.value[0]):
            self.__options_dict.update({key: sorted(temp_dict.get(key), key=lambda o: o.name.lower())})

    def get_options(self) -> dict[Category, list[OptionToggle]]:
        """
        Gets a dictionary of OptionToggles sorted by Category
        :return: Dictionary of OptionToggles
        """
        return self.__options_dict

    def get_options_active(self) -> dict[Category, list[OptionToggle]]:
        """
        Gets a dictionary of active OptionToggles sorted by Category
        :return: Dictionary of OptionToggles
        """
        temp_dict: dict[Category, list[OptionToggle]] = {}
        for category in self.__options_dict.keys():
            temp_dict.update({category: [o for o in self.__options_dict.get(category) if o.check_button.get_active()]})

        return temp_dict

    def get_selected_count(self) -> int:
        """
        Gets the current number of selected options
        :return: Int that denotes the number of selected options
        """
        selected_count = 0
        for option_list in self.get_options_active().values():
            selected_count += len(option_list)

        return selected_count

    def get_selected_string(self) -> str:
        """
        Gets a string that shows how many options are currently selected
        :return: String that shows how many options are currently selected, example: "Selected: 14/100"
        """
        return f"Selected: {self.get_selected_count()}/{self.__option_count}"

    def profile_load(self, file_path: str) -> bool:
        """
        Loads a profile file and sets the options in the OptionStore to match
        :param file_path: Path to the profile file, example: "/home/user/downloads/test.profile"
        :return: True if load was successful, False if not
        """
        try:
            with open(file_path, "r") as import_file:
                profile_data: dict[str, list[str]] = json.load(import_file)
                for category in self.__options_dict.keys():
                    profile_options = profile_data.get(category.value[0])
                    for option in self.__options_dict.get(category):
                        if not option.can_toggle:
                            continue
                        option.check_button.set_active(option.name in profile_options)
            print(f"Loaded profile from: '{file_path}'")
            return True
        except Exception as err:
            print(f"Unable to load profile: {err}")
            return False

    def profile_save(self, file_path: str):
        """
        Saves the current state of the OptionStore to a profile file
        :param file_path: Path to the profile file, example: "/home/user/downloads/test.profile"
        :return: None
        """
        active_options = self.get_options_active()
        profile_data: dict[str, list[str]] = {}
        for category in active_options.keys():
            profile_data.update({category.value[0]: [option.name for option in active_options.get(category)]})

        try:
            with open(file_path, "w") as export_file:
                export_file.write(json.dumps(profile_data, indent=4))
            print(f"Saved profile to: '{file_path}'")
        except Exception as err:
            print(f"Unable to save profile: {err}")

    def set_all(self, new_value: bool):
        """
        Sets all options to a new value, skips options that are disabled
        :param new_value: New value that all options should be set to, example: True
        :return: None
        """
        for category in self.__options_dict.keys():
            self.set_category(category, new_value)

    def set_category(self, category: Category, new_value: bool):
        """
        Sets all options in a category to a new value, skips options that are disabled
        :param category: Category that we want to toggle, example: Category.APPLICATION
        :param new_value: New value that the category options should be set to, example: True
        :return: None
        """
        for option in self.__options_dict.get(category):
            if not option.can_toggle:
                continue

            option.check_button.set_active(new_value)
