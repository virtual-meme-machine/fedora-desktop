import subprocess

from utils.sudo_utils import run_command_as_sudo

FLATHUB_URL: str = "https://flathub.org/repo/flathub.flatpakrepo"
FLATPAK_EXEC: str = "/usr/bin/flatpak"


def __enable_flathub_repo():
    """
    Enables Flathub repo
    :return: None
    """
    repo_dict = __get_repo_dict()
    if "flathub" in repo_dict.keys() and "filtered" not in repo_dict.get("flathub"):
        return

    print(f"Enabling Flathub repo...")
    run_command_as_sudo([FLATPAK_EXEC, "remote-add", "flathub", FLATHUB_URL])


def __get_flatpak_list() -> list[str]:
    """
    Gets a list of flatpaks installed on the system
    :return: List of installed flatpaks
    """
    flatpak_list: list[str] = []

    output = subprocess.run([FLATPAK_EXEC, "list", "--columns=application"],
                            capture_output=True,
                            check=True,
                            text=True).stdout.strip()
    for line in output.split("\n"):
        if line == "Application ID":
            continue

        flatpak_list.append(line)

    return flatpak_list


def __get_repo_dict() -> dict[str, str]:
    """
    Gets a list of flatpak repositories installed on the system
    :return: Dictionary of flatpak repositories, with repo names as keys and repo options as values
    """
    repo_list: dict[str, str] = {}

    output = subprocess.run([FLATPAK_EXEC, "remotes", "--show-disabled"],
                            capture_output=True,
                            check=True,
                            text=True).stdout.strip()
    if output:
        for line in output.split("\n"):
            split = line.split()
            if split[0] == "Name" and split[1] == "Options":
                continue

            repo_list.update({split[0]: split[1]})

    return repo_list


def __remove_fedora_repos():
    """
    Removes the stock Fedora flatpak repos
    :return: None
    """
    repo_dict = __get_repo_dict()
    remove_list: list[str] = []

    if "fedora" in repo_dict.keys():
        remove_list.append("fedora")
    if "fedora-testing" in repo_dict.keys():
        remove_list.append("fedora-testing")
    if "flathub" in repo_dict.keys() and "filtered" in repo_dict.get("flathub"):
        remove_list.append("flathub")

    if not remove_list:
        return

    for repo in remove_list:
        print(f"Removing stock Fedora repo: '{repo}'")
        run_command_as_sudo([FLATPAK_EXEC, "remote-delete", repo, "--force"])


def install_flatpaks(flatpak_list: list[str]):
    """
    Installs the provided list of flatpaks
    :param flatpak_list: List of flatpak IDs that we want to install
    :return: None
    """
    installed_flatpaks = __get_flatpak_list()
    for flatpak in flatpak_list.copy():
        if flatpak in installed_flatpaks:
            flatpak_list.remove(flatpak)

    if not flatpak_list:
        print("Selected flatpaks are already installed")
        return

    __remove_fedora_repos()
    __enable_flathub_repo()

    print(f"Installing flatpaks: {flatpak_list}")
    command = [FLATPAK_EXEC, "install", "flathub", "--noninteractive"] + flatpak_list
    subprocess.run(command, check=True)


def install_updates():
    """
    Checks for available flatpak updates and installs them
    :return: None
    """
    print("Checking for flatpak updates...")
    subprocess.run([FLATPAK_EXEC, "update", "--noninteractive"], check=True)


def is_flatpak_installed(flatpak_id: str) -> bool:
    """
    Checks if the given flatpak is installed
    :param flatpak_id: ID for the flatpak we are checking for
    :return: True if installed, false if not
    """
    return flatpak_id in __get_flatpak_list()
