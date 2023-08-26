from subprocess import CalledProcessError

import utils.dnf_utils as dnf_utils
import utils.flatpak_utils as flatpak_utils
from data.OperationType import OperationType
from gui.OptionToggle import OptionToggle, get_selected_string
from utils.platform_utils import set_gsettings_values
from utils.print_utils import print_header
from utils.script_utils import load_script


def setup(option_list: list[OptionToggle]):
    """
    Setup workflow executed once the 'Begin Setup' button is clicked
    :param option_list: List of OptionToggle objects provided by the GUI
    :return: None
    """
    flatpak_list: list[str] = []
    gsettings_value_list: list[dict] = []
    package_install_list: list[str] = []
    package_install_rpmfusion_list: list[str] = []
    package_remove_list: list[str] = []
    script_list: list[str] = []

    # Process selected options
    for option in option_list:
        if not option.get_active():
            continue

        if option.operation_type is OperationType.FLATPAK:
            flatpak_list.extend(option.operation_args)
        elif option.operation_type is OperationType.GSETTINGS_VALUE:
            gsettings_value_list.extend(option.operation_args)
        elif option.operation_type is OperationType.PACKAGE_INSTALL:
            package_install_list.extend(option.operation_args)
        elif option.operation_type is OperationType.PACKAGE_INSTALL_RPMFUSION:
            package_install_rpmfusion_list.extend(option.operation_args)
        elif option.operation_type is OperationType.PACKAGE_REMOVE:
            package_remove_list.extend(option.operation_args)
        elif option.operation_type is OperationType.SCRIPT:
            script_list.extend(option.operation_args)

    # Print start message
    print_header("Beginning Setup")
    print(get_selected_string(option_list))

    # Check if any packages from RPMFusion are marked for install
    enable_rpmfusion = False
    if package_install_rpmfusion_list:
        package_install_list.extend(package_install_rpmfusion_list)
        enable_rpmfusion = True

    # Install packages
    if package_install_list:
        print_header("Installing Packages")
        try:
            dnf_utils.install_packages(sorted(package_install_list), rpmfusion=enable_rpmfusion)
        except CalledProcessError as err:
            print(f"Package installation failed, {err}")
            exit(1)

    # Install flatpaks
    if flatpak_list:
        print_header("Installing Flatpaks")
        try:
            flatpak_utils.install_flatpaks(flatpak_list)
        except CalledProcessError as err:
            print(f"Flatpak installation failed, {err}")
            exit(1)

    # Execute scripts
    for script in sorted(script_list):
        print_header(f"Executing Script: '{script}'")
        try:
            load_script(script).execute()
        except (ConnectionError, FileNotFoundError, NotADirectoryError, ValueError, CalledProcessError) as err:
            print(f"Script '{script}' failed, {err}")
            exit(1)

    # Apply Gsettings values
    if gsettings_value_list:
        print_header("Applying Settings")
        try:
            set_gsettings_values(sorted(gsettings_value_list, key=lambda i: i.get("schema").lower()))
        except CalledProcessError as err:
            print(f"Failed to apply settings, {err}")
            exit(1)

    # Remove packages
    if package_remove_list:
        print_header("Removing Packages")
        try:
            dnf_utils.remove_packages(sorted(package_remove_list))
        except CalledProcessError as err:
            print(f"Package removal failed, {err}")
            exit(1)

    # Print finished message
    print_header("Setup Complete")
    print("The system will need to be restarted in order for most changes to take effect.")
    print("Enjoy!")
