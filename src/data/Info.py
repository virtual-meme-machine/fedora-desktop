import subprocess

from data.Paths import PACKAGE_ROOT

APPLICATION_AUTHOR: str = "virtual-meme-machine"
APPLICATION_ID: str = "com.virtual.meme.machine.fedora.setup"
APPLICATION_NAME: str = "Fedora Desktop Configurator"
APPLICATION_VERSION: str = "3.3"

SUPPORTED_FEDORA_VERSIONS: list[int] = [37, 38]


def get_application_version() -> str:
    """
    Gets the application version
    :return: String containing the application's version
    """
    try:
        git_commit = subprocess.check_output(["/usr/bin/git", "rev-parse", "--short", "HEAD"],
                                             cwd=PACKAGE_ROOT,
                                             stderr=subprocess.DEVNULL,
                                             text=True).strip()
        return f"{APPLICATION_VERSION}-git-{git_commit}"
    except:
        return APPLICATION_VERSION
