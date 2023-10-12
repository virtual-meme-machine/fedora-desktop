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

    output = subprocess.run(["/usr/bin/xdg-settings", "get", "default-web-browser"],
                            capture_output=True,
                            check=True,
                            text=True).stdout.strip()
    if output == BROWSER_DESKTOP:
        print(f"Default web browser already set")
        return

    print(f"Setting default web browser to '{BROWSER_DESKTOP}'")
    subprocess.run(["/usr/bin/xdg-settings", "set", "default-web-browser", BROWSER_DESKTOP], check=True)
