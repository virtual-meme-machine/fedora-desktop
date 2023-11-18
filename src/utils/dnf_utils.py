import subprocess

from utils.platform_utils import get_fedora_version
from utils.sudo_utils import run_command_as_sudo

DNF_EXEC: str = "/usr/bin/dnf"
DNF_NON_INTERACTIVE_FLAG: str = "--assumeyes"


def __enable_rpmfusion_repos():
    """
    Enables RPMFusion repos
    :return: None
    """
    repo_list = __get_repo_list()
    package_list: list[str] = []

    if "rpmfusion-free" not in repo_list:
        package_list.append(f"https://download1.rpmfusion.org/free/fedora/"
                            f"rpmfusion-free-release-{get_fedora_version()}.noarch.rpm")
    if "rpmfusion-nonfree" not in repo_list:
        package_list.append(f"https://download1.rpmfusion.org/nonfree/fedora/"
                            f"rpmfusion-nonfree-release-{get_fedora_version()}.noarch.rpm")

    if package_list:
        print("Enabling RPMFusion repos...")
        install_packages(package_list)


def __get_package_list() -> list[str]:
    """
    Gets a list of packages installed on the system
    :return: List of installed packages
    """
    package_list: list[str] = []

    output = subprocess.run([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "list", "installed"],
                            capture_output=True, check=True, text=True).stdout.strip()
    for line in output.split("\n"):
        if line == "Installed Packages":
            continue

        package_list.append(line.split()[0].split(".")[0])

    return package_list


def __get_repo_list() -> list[str]:
    """
    Gets a list of package repositories installed on the system
    :return: List of package repositories
    """
    repo_list: list[str] = []

    output = subprocess.run([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "repolist"],
                            capture_output=True, check=True, text=True).stdout.strip()
    for line in output.split("\n"):
        if "repo id" in line and "repo name" in line:
            continue

        repo_list.append(line.split()[0])

    return repo_list


def __wildcard_check(installed_packages: list[str], wildcard_string: str) -> bool:
    """
    Checks if any packages in the installed packages list contain the wildcard string
    :param installed_packages: List of installed package names
    :param wildcard_string: String containing a wildcard character, eg: "libreoffice*"
    :return: True if present, False if not
    """
    wildcard_string = wildcard_string.strip("*")
    for installed_package in installed_packages:
        if wildcard_string in installed_package:
            return True

    return False


def auto_remove_packages():
    """
    Automatically removes unused dependency packages
    :return: None
    """
    print("Checking for unused dependency packages...")
    check = subprocess.run([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "list", "autoremove"],
                           capture_output=True, check=True, text=True).stdout

    if "Autoremove Packages" not in check:
        print("No unused dependencies to remove")
        return

    run_command_as_sudo([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "autoremove"])


def install_packages(package_list: list[str], rpmfusion: bool = False):
    """
    Installs the provided list of packages
    :param package_list: List of package names that we want to install
    :param rpmfusion: Boolean that denotes if the packages come from RPMFusion
    :return: None
    """
    installed_packages = __get_package_list()
    for package in package_list.copy():
        if package in installed_packages:
            package_list.remove(package)

    if not package_list:
        print("Selected packages are already installed")
        return

    if rpmfusion:
        __enable_rpmfusion_repos()

    print(f"Installing RPM packages: {package_list}")
    run_command_as_sudo([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "install"] + package_list)


def install_updates():
    """
    Checks for available package updates and installs them
    :return: None
    """
    print("Checking for package updates...")
    check = subprocess.run([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "check-update", "--refresh"],
                           stdout=subprocess.DEVNULL)

    if check.returncode == 0:
        print("No updates available")
        return

    run_command_as_sudo([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "update", "--refresh"])


def is_package_installed(package_name: str) -> bool:
    """
    Checks if the given package is installed
    :param package_name: Name of the package we are checking for
    :return: True if installed, false if not
    """
    return package_name in __get_package_list()


def remove_packages(package_list: list[str]):
    """
    Removes the provided list of packages
    :param package_list: List of package names that we want to remove
    :return: None
    """
    installed_packages = __get_package_list()
    for package in package_list.copy():
        if "*" in package:
            if not __wildcard_check(installed_packages, package):
                package_list.remove(package)
            continue

        if package not in installed_packages:
            package_list.remove(package)

    if not package_list:
        print("Selected packages have already been removed")
        return

    print(f"Removing RPM packages: {package_list}")
    run_command_as_sudo([DNF_EXEC, DNF_NON_INTERACTIVE_FLAG, "remove"] + package_list)
