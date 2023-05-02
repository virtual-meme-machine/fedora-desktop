import utils.dnf_utils as dnf_utils
import utils.flatpak_utils as flatpak_utils
import utils.gnome_extension_utils as gnome_extension_utils
from data.OperationType import OperationType
from gui.OptionToggle import OptionToggle
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
    gnome_extension_list: list[str] = []
    gsettings_value_list: list[dict] = []
    package_install_list: list[str] = []
    package_install_rpmfusion_list: list[str] = []
    package_remove_list: list[str] = []
    script_list: list[str] = []

    # Process selected options
    enabled_count = 0
    for option in option_list:
        if not option.check_button.get_active():
            continue

        enabled_count += 1
        if option.operation_type is OperationType.FLATPAK:
            flatpak_list.extend(option.operation_args)
        elif option.operation_type is OperationType.GNOME_EXTENSION:
            gnome_extension_list.extend(option.operation_args)
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
    print(f"{enabled_count}/{len(option_list)} options selected")

    # Remove packages
    if package_remove_list:
        print_header("Removing Packages")
        dnf_utils.remove_packages(sorted(package_remove_list))

    # Check if any packages from RPMFusion are marked for install
    enable_rpmfusion = False
    if package_install_rpmfusion_list:
        package_install_list.extend(package_install_rpmfusion_list)
        enable_rpmfusion = True

    # Install packages
    if package_install_list:
        print_header("Installing Packages")
        dnf_utils.install_packages(sorted(package_install_list), rpmfusion=enable_rpmfusion)

    # Install flatpaks
    if flatpak_list:
        print_header("Installing Flatpaks")
        flatpak_utils.install_flatpaks(flatpak_list)

    # Install Gnome Shell extensions
    if gnome_extension_list:
        print_header("Installing Gnome Shell Extensions")
        gnome_extension_utils.install_extensions(gnome_extension_list)
        gnome_extension_utils.enable_extensions(gnome_extension_list)

    # Execute scripts
    for script in sorted(script_list):
        print_header(f"Executing Script: '{script}'")
        load_script(script).execute()

    # Apply Gsettings values
    if gsettings_value_list:
        print_header("Applying Settings")
        set_gsettings_values(sorted(gsettings_value_list, key=lambda i: i.get("schema").lower()))

    # Print finished message
    print_header("Setup Complete")
    print("The system will need to be restarted in order for most changes to take effect.")
    print("Enjoy!")
