import json
import os
import platform
import subprocess

GSETTINGS_EXEC: str = "/usr/bin/gsettings"
GSETTINGS_GET_REMOVE_VALUES: list[str] = ["@as", "uint32"]
LOCAL_BIN: str = os.path.expanduser("~/.local/bin")
SCRIPT_MAIN_VERSION: str = "3.0"


def get_fedora_version() -> int:
    """
    Gets the version of Fedora on this system
    :return: Integer that represents the Fedora version, eg: 38
    """
    return int(platform.freedesktop_os_release().get("VERSION_ID"))


def get_gnome_version() -> int:
    """
    Gets the version of Gnome Shell on this system
    :return: Integer that represents the Gnome Shell version, eg: 44
    """
    return int(subprocess.check_output(["gnome-shell", "--version"], text=True).strip().split()[2].split(".")[0])


def get_gsettings_json(schema: str, key: str) -> list or dict:
    """
    Gets JSON data from Gsettings, loads it, and returns it
    :param schema: Schema for the Gsettings value we want to get
    :param key: Key for the specific Gsettings value in the schema
    :return: Retrieved deserialized JSON data, likely a list or dictionary
    """
    output = subprocess.check_output([GSETTINGS_EXEC, "get", schema, key], text=True).strip().replace("'", "\"")

    for value in GSETTINGS_GET_REMOVE_VALUES:
        if value in output:
            output = output.replace(value, "")

    return json.loads(output.strip())


def get_gsettings_value(schema: str, key: str) -> str:
    """
    Gets a Gsettings value
    :param schema: Schema for the Gsettings value we want to get
    :param key: Key for the specific Gsettings value in the schema
    :return: Retrieved Gsettings value
    """
    output = subprocess.check_output([GSETTINGS_EXEC, "get", schema, key], text=True).strip()

    for value in GSETTINGS_GET_REMOVE_VALUES:
        if value in output:
            output = output.replace(value, "")

    return output.strip()


def get_distro_full_name() -> str:
    """
    Gets the distro's full name
    :return: String containing the full name of the system's distro, eg: "Fedora Linux 38 (Workstation Edition)"
    """
    return platform.freedesktop_os_release().get("PRETTY_NAME")


def get_script_version() -> str:
    """
    Gets the version of this script
    :return: String containing this script's version
    """
    try:
        git_commit = subprocess.check_output(["/usr/bin/git", "rev-parse", "--short", "HEAD"],
                                             stderr=subprocess.DEVNULL,
                                             text=True).strip()
        return f"{SCRIPT_MAIN_VERSION}-git-{git_commit}"
    except:
        return SCRIPT_MAIN_VERSION


def is_application_installed(application_desktop: str) -> bool:
    """
    Checks if a .desktop file exists for the given application
    :param application_desktop: Name of the applications .desktop file
    :return: True if found, False if not
    """
    xdg_data_dirs = os.environ.get("XDG_DATA_DIRS").split(":")
    if os.path.expanduser("~/.local/share") not in xdg_data_dirs:
        xdg_data_dirs.append(os.path.expanduser("~/.local/share"))

    for path in xdg_data_dirs:
        applications_path = os.path.join(path, "applications")
        if not os.path.isdir(applications_path):
            continue

        if application_desktop in os.listdir(applications_path):
            return True

    return False


def is_exec_in_path(exec_name: str) -> bool:
    """
    Checks if the given exec is accessible via $PATH
    :param exec_name: Name of the exec we are looking for, eg: "dnf"
    :return: True if found, False if not
    """
    path_dirs = os.get_exec_path()

    for path in path_dirs:
        if not os.path.isdir(path):
            continue

        if exec_name in os.listdir(path):
            return True

    return False


def set_gsettings_json(schema: str, key: str, value: list or dict):
    """
    Sets a Gsettings value with provided deserialized JSON data
    :param schema: Schema for the Gsettings value we want to change
    :param key: Key for the specific Gsettings value in the schema
    :param value: Deserialized JSON data, likely a list or dictionary
    :return: None
    """
    set_gsettings_value(schema=schema, key=key, value=json.dumps(value).replace("\"", "'"))


def set_gsettings_value(schema: str, key: str, value: str):
    """
    Sets a Gsettings value
    :param schema: Schema for the Gsettings value we want to change
    :param key: Key for the specific Gsettings value in the schema
    :param value: Value that should be stored in Gsettings
    :return: None
    """
    if get_gsettings_value(schema=schema, key=key) == value:
        return

    print(f"Applying Gsettings value: [Schema: '{schema}', Key: '{key}', Value: '{value}']")
    subprocess.check_call([GSETTINGS_EXEC, "set", schema, key, value])


def set_gsettings_values(gsettings_list: list[dict]):
    """
    Applies a list of Gsettings values
    :param gsettings_list: List of dictionaries each containing a Gsettings schema, key, and value
    :return: None
    """
    for setting in gsettings_list.copy():
        if get_gsettings_value(schema=setting.get("schema"), key=setting.get("key")) == setting.get("value"):
            gsettings_list.remove(setting)

    if not gsettings_list:
        print("No changes to apply")
        return

    for setting in gsettings_list:
        set_gsettings_value(schema=setting.get("schema"),
                            key=setting.get("key"),
                            value=setting.get("value"))


def symlink_to_local_bin(exec_path: str):
    """
    Symlinks an exec to the user's local bin directory
    :param exec_path: Path to the exec we want to symlink
    :return: None
    """
    exec_name = os.path.basename(exec_path)
    bin_exec_path = os.path.join(LOCAL_BIN, exec_name)

    if is_exec_in_path(exec_name):
        print(f"Exec '{exec_name}' already in a valid PATH")
        return

    if not os.path.exists(LOCAL_BIN):
        os.makedirs(LOCAL_BIN)

    if not os.path.isdir(LOCAL_BIN):
        raise NotADirectoryError(f"Local bin folder '{LOCAL_BIN}' is not a directory")

    if not os.path.isfile(exec_path):
        raise FileNotFoundError(f"Unable to locate exec '{exec_path}'")

    print(f"Symlinking exec '{exec_name}' to '{LOCAL_BIN}'")
    os.symlink(src=exec_path, dst=bin_exec_path)
