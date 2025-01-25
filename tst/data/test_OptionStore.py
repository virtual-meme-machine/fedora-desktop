import json
import os
import tempfile
from unittest.mock import patch

from data import Category
from data import OperationType
from data import OptionStore
from data import Option
from utils.file_utils import delete_path

TEST_OPTION_DATA: dict = {
    "name": "Archive Manager",
    "description": "Advanced archive manager",
    "documentation_link": "testing123",
    "default_state": True,
    "unsupported_versions": [0],
    "category": "application",
    "actions": [
        {
            "operation_type": "package_install",
            "operation_args": [
                "file-roller"
            ]
        }
    ]
}
TEST_PROFILE_DATA: dict = {
    "application": [
        "Archive Manager"
    ]
}


def mock_get_fedora_version_unsupported() -> int:
    """
    Mocked platform_utils.get_fedora_version()
    :return: Unsupported version number
    """
    return 0


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import data.OptionStore  # noqa: F401


class TestOptionStore:
    """
    Tests the OptionStore class
    Generates the following files in a temp dir on initialization:
    - valid.json
    - valid.profile
    - invalid.txt
    """
    temp_dir = tempfile.mkdtemp()
    option_file = os.path.join(temp_dir, "valid.json")
    profile_file = os.path.join(temp_dir, "valid.profile")
    invalid_file = os.path.join(temp_dir, "invalid.txt")

    with open(option_file, "w") as file:
        file.write(json.dumps([TEST_OPTION_DATA], indent=4))
    with open(profile_file, "w") as file:
        file.write(json.dumps(TEST_PROFILE_DATA, indent=4))
    with open(invalid_file, "w") as file:
        file.write(json.dumps([{"invalid": True}], indent=4))

    option_store = OptionStore.OptionStore(options_dir=temp_dir)

    def __del__(self):
        """
        Cleans up generated files when class is de-initialized
        :return: None
        """
        delete_path(self.temp_dir)

    def test_get_options(self):
        """
        Tests OptionStore.get_options() with the following use cases:
        - OptionStore imports valid.json
        - OptionStore ignores other files
        - OptionStore.get_options() returns dict[Category, list[OptionToggle]]
        - OptionStore.get_options() contains the expected number of entries
        - OptionStore.get_options() contains valid entries
        :return: None
        """
        options = self.option_store.get_options()
        options_sub_list = options.get(Category.Category.APPLICATION)
        option = options_sub_list[0]

        assert type(options) is dict
        assert type(options_sub_list) is list
        assert type(option) is Option.Option

        assert len(options_sub_list) == 1

        assert type(option.name) is str
        assert option.name == TEST_OPTION_DATA.get("name")

        assert type(option.description) is str
        assert option.description == TEST_OPTION_DATA.get("description")

        assert type(option.default_state) is bool
        assert option.default_state == TEST_OPTION_DATA.get("default_state")

        assert type(option.can_toggle) is bool
        assert option.can_toggle is True
        assert option.check_button.get_sensitive() is True

        assert type(option.category) is Category.Category
        assert option.category.value[0] == TEST_OPTION_DATA.get("category")

        assert type(option.actions) is list
        assert type(option.actions[0].operation_type) is OperationType.OperationType
        assert option.actions[0].operation_type.value == TEST_OPTION_DATA.get("actions")[0].get("operation_type")

        assert type(option.actions[0].operation_args) is list
        assert option.actions[0].operation_args == TEST_OPTION_DATA.get("actions")[0].get("operation_args")

    @patch("data.Option.get_fedora_version", new=mock_get_fedora_version_unsupported)
    def test_get_options_unsupported(self):
        """
        Tests OptionStore.get_options() with the following use cases:
        - Unsupported option is not enabled
        :return: None
        """
        option_store = OptionStore.OptionStore(options_dir=self.temp_dir)

        options = option_store.get_options()
        options_sub_list = options.get(Category.Category.APPLICATION)
        option = options_sub_list[0]

        assert option.default_state is False
        assert option.can_toggle is False
        assert option.check_button.get_sensitive() is False

    def test_get_options_active(self):
        """
        Tests OptionStore.get_options_active() with the following use cases:
        - OptionStore.get_options_active() returns option when check_button active is set to true
        - OptionStore.get_options_active() does not return option when check_button active is set to false
        :return: None
        """
        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(True)
        assert len(self.option_store.get_options_active().get(Category.Category.APPLICATION)) == 1

        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(False)
        assert len(self.option_store.get_options_active().get(Category.Category.APPLICATION)) == 0

    def test_get_selected_count(self):
        """
        Tests OptionStore.get_selected_count() with the following use cases:
        - OptionStore.get_selected_count() count includes option when check_button active is set to true
        - OptionStore.get_selected_count() count does not include option when check_button active is set to false
        :return: None
        """
        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(True)
        assert self.option_store.get_selected_count() == 1

        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(False)
        assert self.option_store.get_selected_count() == 0

    def test_get_selected_string(self):
        """
        Tests OptionStore.get_selected_string() with the following use cases:
        - OptionStore.get_selected_string() count includes option when check_button active is set to true
        - OptionStore.get_selected_string() count does not include option when check_button active is set to false
        :return: None
        """
        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(True)
        assert self.option_store.get_selected_string() == f"Selected: 1/1"

        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(False)
        assert self.option_store.get_selected_string() == f"Selected: 0/1"

    def test_profile_load(self):
        """
        Tests OptionStore.profile_load() with the following use cases:
        - OptionStore.profile_load() loading valid file returns True
        - OptionStore.profile_load() loading invalid file returns False
        - OptionStore.profile_load() loading valid file toggles check_button state to match profile
        :return: None
        """
        assert self.option_store.profile_load(file_path=self.profile_file) is True
        assert self.option_store.profile_load(file_path=self.invalid_file) is False

        self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.set_active(False)
        assert self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.get_active() is False
        self.option_store.profile_load(file_path=self.profile_file)
        assert self.option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.get_active() is True

    @patch("data.Option.get_fedora_version", new=mock_get_fedora_version_unsupported)
    def test_profile_load_unsupported(self):
        """
        Tests OptionStore.profile_load() with the following use cases:
        - OptionStore.profile_load() does not enable unsupported option
        :return: None
        """
        option_store = OptionStore.OptionStore(options_dir=self.temp_dir)

        assert option_store.profile_load(file_path=self.profile_file) is True
        assert option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.get_active() is False

    def test_profile_save(self, capfd):
        """
        Tests OptionStore.profile_save() with the following use cases:
        - OptionStore.profile_save() with valid file path saves valid file
        - OptionStore.profile_save() File contents contains the data from the OptionStore
        - OptionStore.profile_save() with invalid file path prints error message
        :param capfd: pytest capture object
        :return: None
        """
        test_file = os.path.join(self.temp_dir, "test.profile")
        self.option_store.profile_load(file_path=self.profile_file)

        self.option_store.profile_save(file_path=test_file)
        with open(self.profile_file, "r") as file1, open(test_file, "r") as file2:
            assert file1.read() == file2.read()

        self.option_store.profile_save(file_path="/")
        out, err = capfd.readouterr()
        assert "Unable to save profile" in out

    def test_set_all(self):
        """
        Tests OptionStore.set_all() with the following use cases:
        - OptionStore.set_all(True) sets all options to True
        - OptionStore.set_all(False) sets all options to False
        :return: None
        """
        self.option_store.set_all(new_value=True)
        assert all(all(option.check_button.get_active() is True for option in option_list)
                   for option_list in self.option_store.get_options().values())

        self.option_store.set_all(new_value=False)
        assert all(all(option.check_button.get_active() is False for option in option_list)
                   for option_list in self.option_store.get_options().values())

    @patch("data.Option.get_fedora_version", new=mock_get_fedora_version_unsupported)
    def test_set_all_unsupported(self):
        """
        Tests OptionStore.set_all() with the following use cases:
        - OptionStore.set_all(True) does not enable unsupported options
        :return: None
        """
        option_store = OptionStore.OptionStore(options_dir=self.temp_dir)

        option_store.set_all(new_value=True)
        assert option_store.get_options().get(Category.Category.APPLICATION)[0].check_button.get_active() is False
