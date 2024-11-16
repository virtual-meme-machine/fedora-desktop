import subprocess

from data.Paths import PACKAGE_ROOT

APPLICATION_AUTHOR: str = "virtual-meme-machine"
APPLICATION_ID: str = "com.virtual.meme.machine.fedora.setup"
APPLICATION_NAME: str = "Fedora Desktop Configurator"
APPLICATION_VERSION: str = "3.4.3"

SUPPORTED_FEDORA_VERSIONS: list[int] = [41]


def get_application_version(package_root: str = PACKAGE_ROOT) -> str:
    """
    Gets the application version
    :param package_root: Path to the root of the package, example: "/home/user/fedora-desktop"
    :return: String containing the application's version
    """
    try:
        git_commit = subprocess.run(["/usr/bin/git", "rev-parse", "--short", "HEAD"],
                                    capture_output=True,
                                    check=True,
                                    cwd=package_root,
                                    text=True).stdout.strip()
        return f"{APPLICATION_VERSION}-git-{git_commit}"
    except:
        return APPLICATION_VERSION
