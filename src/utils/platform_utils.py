import configparser
import json
import os
import platform
import subprocess

DCONF_EXEC: str = "/usr/bin/dconf"
GSETTINGS_EXEC: str = "/usr/bin/gsettings"
LOCAL_BIN: str = os.path.expanduser("~/.local/bin")
REMOVE_VALUES: list[str] = ["@as", "uint32"]

XDG_DATA_DIRS = os.environ.get("XDG_DATA_DIRS").split(":")
if os.path.expanduser("~/.local/share") not in XDG_DATA_DIRS:
    XDG_DATA_DIRS.append(os.path.expanduser("~/.local/share"))


def __get_desktop_file(application_desktop: str) -> str or None:
    """
    Gets the path to an application's .desktop file
    :param application_desktop: Name of the application's .desktop file
    :return: Path to the .desktop file if it could be found, None if not
    """
    for path in XDG_DATA_DIRS:
        applications_path = os.path.join(path, "applications")
        if not os.path.isdir(applications_path):
            continue

        desktop_file = os.path.join(applications_path, application_desktop)
        if os.path.isfile(desktop_file):
            return desktop_file

    print(f"Unable to locate application: '{application_desktop}'")
    return None


def get_application_name(application_desktop: str) -> str or None:
    """
    Gets the readable name for an application by parsing its .desktop file
    :param application_desktop: Name of the application's .desktop file
    :return: Name of the application if it is installed, None if not
    """
    config_path = __get_desktop_file(application_desktop)
    if config_path is None:
        return None

    config = configparser.ConfigParser()
    config.read(config_path)

    if "name" not in config["Desktop Entry"].keys():
        return None

    return config.get(section="Desktop Entry", option="name")


def get_application_categories(application_desktop: str) -> list[str] or None:
    """
    Gets the readable name for an application by parsing its .desktop file
    :param application_desktop: Name of the application's .desktop file
    :return: Name of the application if it is installed, None if not
    """
    config_path = __get_desktop_file(application_desktop)
    if config_path is None:
        return None

    config = configparser.ConfigParser()
    config.read(config_path)

    if "categories" not in config["Desktop Entry"].keys():
        return None

    return config.get(section="Desktop Entry", option="categories").split(";")


def get_distro_full_name() -> str:
    """
    Gets the distro's full name
    :return: String containing the full name of the system's distro, eg: "Fedora Linux 38 (Workstation Edition)"
    """
    return platform.freedesktop_os_release().get("PRETTY_NAME")


def get_dconf_value(key: str) -> str:
    """
    Gets a dconf value
    :param key: Key for the specific dconf value in the schema
    :return: Retrieved dconf value
    """
    output = subprocess.run([DCONF_EXEC, "read", key], capture_output=True, text=True).stdout.strip()

    for value in REMOVE_VALUES:
        if value in output:
            output = output.replace(value, "")

    return output.strip()


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
    return int(subprocess.run(["/usr/bin/gnome-shell", "--version"],
                              capture_output=True,
                              text=True).stdout.strip().split()[2].split(".")[0])


def get_gsettings_json(schema: str, key: str) -> list or dict:
    """
    Gets JSON data from Gsettings, loads it, and returns it
    :param schema: Schema for the Gsettings value we want to get
    :param key: Key for the specific Gsettings value in the schema
    :return: Retrieved deserialized JSON data, likely a list or dictionary
    """
    output = subprocess.run([GSETTINGS_EXEC, "get", schema, key],
                            capture_output=True,
                            text=True).stdout.strip().replace("'", "\"")

    for value in REMOVE_VALUES:
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
    output = subprocess.run([GSETTINGS_EXEC, "get", schema, key], capture_output=True, text=True).stdout.strip()

    for value in REMOVE_VALUES:
        if value in output:
            output = output.replace(value, "")

    return output.strip()


def get_installed_applications() -> list[str]:
    """
    Gets a list of .desktop files for installed applications
    :return: List of application .desktop files
    """
    application_list = []

    for path in XDG_DATA_DIRS:
        applications_path = os.path.join(path, "applications")
        if not os.path.isdir(applications_path):
            continue

        for file in os.listdir(applications_path):
            if os.path.splitext(file)[1] == ".desktop":
                application_list.append(file)

    return application_list


def is_application_installed(application_desktop: str) -> bool:
    """
    Checks if a .desktop file exists for the given application
    :param application_desktop: Name of the applications .desktop file
    :return: True if found, False if not
    """
    return __get_desktop_file(application_desktop) is not None


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


def set_dconf_value(key: str, value: str):
    """
    Sets a dconf value
    :param key: Key for the specific dconf value in the schema
    :param value: Value that should be stored in dconf
    :return: None
    """
    if get_dconf_value(key=key) == value:
        return

    print(f"Applying dconf value: [Key: '{key}', Value: '{value}']")
    subprocess.run([DCONF_EXEC, "write", key, value], check=True)


def set_dconf_values(setting_list: list[dict]):
    """
    Applies a list of dconf values
    :param setting_list: List of dictionaries each containing a dconf key and value
    :return: None
    """
    for setting in setting_list.copy():
        if get_dconf_value(key=setting.get("key")) == setting.get("value"):
            setting_list.remove(setting)

    if not setting_list:
        print("No changes to apply")
        return

    for setting in setting_list:
        set_dconf_value(key=setting.get("key"),
                        value=setting.get("value"))


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
    subprocess.run([GSETTINGS_EXEC, "set", schema, key, value], check=True)


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
