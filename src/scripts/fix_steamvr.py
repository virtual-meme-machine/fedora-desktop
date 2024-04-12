import json
import os

from utils.dnf_utils import is_package_installed

STEAMVR_FOLDER: str = os.path.expanduser("~/.steam/steam/steamapps/common/SteamVR")
STEAMVR_VRSETTINGS: str = os.path.expanduser("~/.steam/steam/config/steamvr.vrsettings")


def __fix_blank_windows():
    """
    Fixes blank windows opening with SteamVR: https://github.com/ValveSoftware/SteamVR-for-Linux/issues/577
    :return: None
    """
    for json_file in ["drivers/lighthouse/resources/webhelperoverlays.json", "resources/webhelperoverlays.json"]:
        file_path = os.path.join(STEAMVR_FOLDER, json_file)
        if not os.path.isfile(file_path):
            continue

        print(f"Disabling desktop window preload in SteamVR configuration file: {file_path}")
        with open(file_path, "r+") as file:
            file_contents: dict = json.loads(file.read())
            file_modified = False
            for key in file_contents.keys():
                value = file_contents.get(key)
                if isinstance(value, dict) and "preload" in value.keys() and value.get("preload") is True:
                    value.update({"preload": False})
                    file_contents.update({key: value})
                    file_modified = True

            if file_modified:
                print(f"Writing updated configuration file")
                file.seek(0)
                file.write(json.dumps(file_contents, indent=4, sort_keys=True))
                file.truncate()
            else:
                print(f"Preload is already disabled, skipping")

    if os.path.isfile(STEAMVR_VRSETTINGS):
        print(f"Removing all saved DesktopUI windows from SteamVR settings file: {STEAMVR_VRSETTINGS}")
        with open(STEAMVR_VRSETTINGS, "r+") as file:
            file_contents: dict = json.loads(file.read())
            if isinstance(file_contents.get("DesktopUI"), dict) and len(file_contents.get("DesktopUI").keys()) > 0:
                print(f"Writing updated SteamVR settings file")
                file_contents.update({"DesktopUI": {}})
                file.seek(0)
                file.write(json.dumps(file_contents, indent=4, sort_keys=True))
                file.truncate()
            else:
                print(f"No saved DesktopUI windows found, skipping")


def execute():
    """
    Applies various fixes to address known issues with SteamVR for Linux
    :return: None
    """
    if not is_package_installed("steam"):
        print("Steam is not installed, unable to configure SteamVR")
        return

    if not os.path.isdir(STEAMVR_FOLDER):
        print("SteamVR does not appear to be installed, please install it before running this script")
        return

    __fix_blank_windows()
