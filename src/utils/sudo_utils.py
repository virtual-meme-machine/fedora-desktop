import base64
import subprocess

from utils.caffeine_utils import deactivate_caffeine_exit
from utils.zenity_utils import prompt_password

__SUDO_PASSWORD: bytes or None = None
SUDO_EXEC: str = "/usr/bin/sudo"


def __verify_sudo_password(password: str) -> bool:
    """
    Verifies the given sudo password by attempting to use it
    :param password: String containing the provided sudo password
    :return: True if able to authenticate, False if not
    """
    try:
        subprocess.run([SUDO_EXEC, "-k", "-S", "/usr/bin/ls"],
                       check=True,
                       input=password.encode(),
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def run_command_as_sudo(args: list[str]):
    """
    Runs a shell command as sudo
    :param args: Command args, example: ["/usr/bin/ls", "-la", "/var/tmp"]
    :return: None
    """
    if __SUDO_PASSWORD is None:
        set_sudo_password()

    subprocess.run([SUDO_EXEC, "-k", "-S", "-p", ""] +
                   args,
                   check=True,
                   input=base64.b64decode(__SUDO_PASSWORD))


def set_sudo_password():
    """
    Prompts the user to provide their password, the stores it as a variable
    :return: None
    """
    while True:
        password = prompt_password()
        if password is None:
            deactivate_caffeine_exit(100)
        elif __verify_sudo_password(password):
            print("Password is valid, temporarily caching")
            global __SUDO_PASSWORD
            __SUDO_PASSWORD = base64.b64encode(password.encode())
            return
        else:
            print("Password is invalid, try again")
