from utils.dnf_utils import __get_repo_list, is_package_installed, install_packages
from utils.file_utils import write_system_file

PACKAGE_NAME: str = "unityhub"
REPO_FILE: str = "/etc/yum.repos.d/unityhub.repo"
REPO_SETTINGS: list[str] = [
    "[unityhub]",
    "name=Unity Hub",
    "baseurl=https://hub.unity3d.com/linux/repos/rpm/stable",
    "enabled=1",
    "gpgcheck=1",
    "gpgkey=https://hub.unity3d.com/linux/repos/rpm/stable/repodata/repomd.xml.key",
    "repo_gpgcheck=1"
]


def __enable_unity_repo():
    """
    Enables the Unity Hub repo
    :return: None
    """
    if PACKAGE_NAME in __get_repo_list():
        print(f"Unity Hub repo already added")
        return

    print("Enabling Unity Hub repo...")
    write_system_file(REPO_FILE, REPO_SETTINGS)


def execute():
    """
    Installs Unity Hub
    Based on: https://docs.unity3d.com/hub/manual/InstallHub.html#install-hub-linux
    :return: None
    """
    if is_package_installed(PACKAGE_NAME):
        print("Unity Hub is already installed")
        return

    __enable_unity_repo()
    install_packages([PACKAGE_NAME])
