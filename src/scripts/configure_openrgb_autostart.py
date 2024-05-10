import json
import os

from utils.flatpak_utils import is_flatpak_installed

PROFILE_NAME: str = "Default"

AUTOSTART_DIR: str = os.path.expanduser("~/.config/autostart")
AUTOSTART_DESKTOP_FILE: str = os.path.join(AUTOSTART_DIR, "org.openrgb.OpenRGB.desktop")
AUTOSTART_DESKTOP_CONTENTS: str = f"""
[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=OpenRGB
Comment=Control RGB lighting
Exec=/usr/bin/flatpak run org.openrgb.OpenRGB --startminimized --profile "{PROFILE_NAME}"
Icon=org.openrgb.OpenRGB
Terminal=false
Categories=Utility;
X-Flatpak-RenamedFrom=OpenRGB.desktop;
X-Flatpak=org.openrgb.OpenRGB
"""

OPENRGB_DATA_DIR: str = os.path.expanduser("~/.var/app/org.openrgb.OpenRGB/config/OpenRGB")
OPENRGB_CONFIG_FILE: str = os.path.join(OPENRGB_DATA_DIR, "OpenRGB.json")
OPENRGB_CONFIG_AUTOSTART_KEY: str = "AutoStart"
OPENRGB_CONFIG_AUTOSTART_DATA: dict = {
    "enabled": True,
    "profile": f"{PROFILE_NAME}",
    "setminimized": True,
    "setprofile": True
}
OPENRGB_PROFILE_FILE: str = os.path.join(OPENRGB_DATA_DIR, f"{PROFILE_NAME}.orp")


def execute():
    """
    Configures OpenRGB to automatically start and apply a default lighting profile on login
    """
    if not is_flatpak_installed("org.openrgb.OpenRGB"):
        print("OpenRGB is not installed, unable to configure autostart")
        return

    # Create autostart directory and OpenRBG data directory if needed
    for directory in [AUTOSTART_DIR, OPENRGB_DATA_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Create autostart .desktop
    if os.path.isfile(AUTOSTART_DESKTOP_FILE):
        print(f"OpenRGB autostart file '{AUTOSTART_DESKTOP_FILE}' already exists")
    else:
        print(f"Generating OpenRGB autostart file at '{AUTOSTART_DESKTOP_FILE}'")
        with open(AUTOSTART_DESKTOP_FILE, "w") as autostart_file:
            autostart_file.write(AUTOSTART_DESKTOP_CONTENTS)

    # Create OpenRGB profile file
    if os.path.isfile(OPENRGB_PROFILE_FILE):
        print(f"OpenRGB profile file '{OPENRGB_PROFILE_FILE}' already exists")
    else:
        print(f"Generating OpenRGB profile file at '{OPENRGB_PROFILE_FILE}'")
        open(OPENRGB_PROFILE_FILE, "w").close()

    # Update OpenRBG config file
    config_data: dict = {}
    if os.path.isfile(OPENRGB_CONFIG_FILE):
        with open(OPENRGB_CONFIG_FILE, "r") as config_file:
            config_data = json.load(config_file)

    if config_data.get(OPENRGB_CONFIG_AUTOSTART_KEY) == OPENRGB_CONFIG_AUTOSTART_DATA:
        print(f"OpenRGB config file '{OPENRGB_CONFIG_FILE}' already contains autostart data")
    else:
        print(f"Adding autostart data to OpenRGB config file '{OPENRGB_CONFIG_FILE}'")
        config_data.update({OPENRGB_CONFIG_AUTOSTART_KEY: OPENRGB_CONFIG_AUTOSTART_DATA})
        with open(OPENRGB_CONFIG_FILE, "w") as config_file:
            config_file.write(json.dumps(config_data, indent=4, sort_keys=True))
