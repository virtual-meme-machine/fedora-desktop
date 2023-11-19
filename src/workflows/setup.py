from subprocess import CalledProcessError

import utils.dnf_utils as dnf_utils
import utils.flatpak_utils as flatpak_utils
from data.Category import Category
from data.OperationType import OperationType
from data.OptionStore import OptionStore
from data.OptionToggle import OptionToggle
from utils.caffeine_utils import activate_caffeine, deactivate_caffeine, deactivate_caffeine_exit
from utils.platform_utils import set_gsettings_values
from utils.print_utils import print_header
from utils.script_utils import load_script
from utils.sudo_utils import set_sudo_password


def setup(option_store: OptionStore):
    """
    Setup workflow executed once the 'Begin Setup' button is clicked
    :param option_store: OptionStore that denotes which actions should be taken
    :return: None
    """
    flatpak_list: list[str] = []
    gsettings_value_list: list[dict] = []
    package_install_list: list[str] = []
    package_install_rpmfusion_list: list[str] = []
    package_remove_list: list[str] = []
    script_list: list[str] = []
    vpn_list: list[OptionToggle] = []

    # Process selected options
    for option_list in option_store.get_options_active().values():
        for option in option_list:
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
                if option.category is Category.VPN:
                    vpn_list.append(option)
                else:
                    script_list.extend(option.operation_args)

    # Check if any packages from RPMFusion are marked for install
    enable_rpmfusion = False
    if package_install_rpmfusion_list:
        package_install_list.extend(package_install_rpmfusion_list)
        enable_rpmfusion = True

    # Print start message
    print_header("Beginning Setup")
    print(option_store.get_selected_string())

    # Activate caffeine to prevent system from going to sleep
    print_header("Activating Caffeine (Prevents Sleep)")
    activate_caffeine()

    # Prompt user for sudo password
    print_header("Prompting for Authentication")
    set_sudo_password()

    # Configure VPN connections
    for vpn_option in vpn_list:
        print_header(f"Configuring VPN Connection: '{vpn_option.name}'")
        for vpn_script in vpn_option.operation_args:
            try:
                load_script(vpn_script).execute()
            except (ConnectionError, CalledProcessError) as err:
                print(f"VPN configuration failed, {err}")
                deactivate_caffeine_exit()

    # Install packages
    if package_install_list:
        print_header("Installing Packages")
        try:
            dnf_utils.install_packages(sorted(package_install_list), rpmfusion=enable_rpmfusion)
        except CalledProcessError as err:
            print(f"Package installation failed, {err}")
            deactivate_caffeine_exit()

    # Install flatpaks
    if flatpak_list:
        print_header("Installing Flatpaks")
        try:
            flatpak_utils.install_flatpaks(flatpak_list)
        except CalledProcessError as err:
            print(f"Flatpak installation failed, {err}")
            deactivate_caffeine_exit()

    # Execute scripts
    for script in sorted(script_list):
        print_header(f"Executing Script: '{script}'")
        try:
            load_script(script).execute()
        except (ConnectionError, FileNotFoundError, NotADirectoryError, ValueError, CalledProcessError) as err:
            print(f"Script '{script}' failed, {err}")
            deactivate_caffeine_exit()

    # Apply Gsettings values
    if gsettings_value_list:
        print_header("Applying Settings")
        try:
            set_gsettings_values(sorted(gsettings_value_list, key=lambda i: i.get("schema").lower()))
        except CalledProcessError as err:
            print(f"Failed to apply settings, {err}")
            deactivate_caffeine_exit()

    # Remove packages
    if package_remove_list:
        print_header("Removing Packages")
        try:
            dnf_utils.remove_packages(sorted(package_remove_list))
        except CalledProcessError as err:
            print(f"Package removal failed, {err}")
            deactivate_caffeine_exit()

    # Deactivate caffeine
    print_header("Deactivating Caffeine (Prevents Sleep)")
    deactivate_caffeine()

    # Print finished message
    print_header("Setup Complete")
    print("The system will need to be restarted in order for most changes to take effect.")
    print("Enjoy!")
