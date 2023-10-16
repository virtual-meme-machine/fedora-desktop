import base64
import subprocess

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
        try:
            print("Please enter your password in the prompt window")
            password = subprocess.run(["/usr/bin/zenity", "--password",
                                       "--modal",
                                       "--title=Authentication Required",
                                       "--ok-label=Submit"], capture_output=True, check=True, text=True).stdout.strip()

            if __verify_sudo_password(password):
                print("Password is valid, temporarily caching")
                global __SUDO_PASSWORD
                __SUDO_PASSWORD = base64.b64encode(password.encode())
                return
            else:
                print("Password is invalid, try again")
        except subprocess.CalledProcessError as err:
            if err.returncode == 1:
                print("Authentication cancelled, exiting")
                exit(100)
