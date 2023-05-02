import subprocess

from utils.platform_utils import is_application_installed

BROWSER_DESKTOP: str = "io.gitlab.librewolf-community.desktop"


def execute():
    """
    Sets the default web browser
    :return: None
    """
    if not is_application_installed(BROWSER_DESKTOP):
        print(f"'{BROWSER_DESKTOP}' is not installed, unable to set default web browser.")
        return

    if subprocess.check_output(
            ["/usr/bin/xdg-settings", "get", "default-web-browser"], text=True).strip() == BROWSER_DESKTOP:
        print(f"Default web browser already set")
        return

    print(f"Setting default web browser to '{BROWSER_DESKTOP}'")
    subprocess.check_call(["/usr/bin/xdg-settings", "set", "default-web-browser", BROWSER_DESKTOP])
