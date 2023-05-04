import subprocess

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
    subprocess.check_call([FLATPAK_EXEC, "remote-add", "flathub", FLATHUB_URL])


def __get_flatpak_list() -> list[str]:
    """
    Gets a list of flatpaks installed on the system
    :return: List of installed flatpaks
    """
    flatpak_list: list[str] = []

    output = subprocess.check_output([FLATPAK_EXEC, "list", "--app", "--columns=application"], text=True).strip()
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

    output = subprocess.check_output([FLATPAK_EXEC, "remotes", "--show-disabled"], text=True).strip()
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
        subprocess.check_call([FLATPAK_EXEC, "remote-delete", repo, "--force"])


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
        print("All selected flatpaks are already installed")
        return

    __remove_fedora_repos()
    __enable_flathub_repo()

    print(f"Installing flatpaks: {flatpak_list}")
    command = [FLATPAK_EXEC, "install", "flathub", "--noninteractive"] + flatpak_list
    subprocess.check_call(command)


def install_updates():
    """
    Checks for available flatpak updates and installs them
    :return: None
    """
    print("Checking for flatpak updates...")
    subprocess.check_call([FLATPAK_EXEC, "update", "--noninteractive"])
