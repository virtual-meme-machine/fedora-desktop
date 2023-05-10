import json
import subprocess

from gi.repository import Gio, GLib

from utils.platform_utils import get_gnome_version, get_gsettings_json, set_gsettings_json

EXTENSION_DOWNLOAD_URL: str = "https://extensions.gnome.org/extension-data"
EXTENSION_INFO_URL: str = "https://extensions.gnome.org/extension-info"
GNOME_EXTENSIONS_EXEC: str = "/usr/bin/gnome-extensions"


def __get_extension_list() -> list[str]:
    """
    Gets a list of Gnome Shell extensions installed on the system
    :return: List of installed Gnome Shell extensions
    """
    extension_list: list[str] = []

    output = subprocess.check_output([GNOME_EXTENSIONS_EXEC, "list"], text=True).strip()
    for line in output.split("\n"):
        extension_list.append(line)

    return extension_list


def enable_extension(extension_id: str):
    """
    Enables a Gnome Shell extension
    :param extension_id: ID for Gnome Shell extension that we want to enable
    :return: None
    """
    enabled_extensions = get_gsettings_json(schema="org.gnome.shell", key="enabled-extensions")

    if extension_id in enabled_extensions:
        print(f"Gnome Shell extension '{extension_id}' is already enabled")
        return

    print(f"Enabling Gnome Shell extension: {extension_id}")
    set_gsettings_json(schema="org.gnome.shell",
                       key="enabled-extensions",
                       value=sorted(enabled_extensions + [extension_id]))


def install_remote_extension(extension_id: str):
    """
    Installs a Gnome Shell extension from the Gnome Extensions website
    :param extension_id: ID for Gnome Shell extension that we want to install
    :return: None
    """
    gnome_shell_version = str(get_gnome_version())
    installed_extensions = __get_extension_list()

    if extension_id in installed_extensions:
        print(f"Gnome Shell extension '{extension_id}' is already installed")
        return

    info = json.loads(subprocess.check_output(["/usr/bin/curl", "-LsS", f"{EXTENSION_INFO_URL}?uuid={extension_id}"]))
    if gnome_shell_version not in info.get("shell_version_map").keys():
        raise ValueError(f"Extension '{extension_id}' does not support Gnome Shell version {gnome_shell_version}")

    print(f"Installing Gnome Shell extension: {extension_id}")
    shell_dbus = Gio.DBusProxy.new_for_bus_sync(
        bus_type=Gio.BusType.SESSION,
        flags=Gio.DBusProxyFlags.NONE,
        info=None,
        name="org.gnome.Shell",
        object_path="/org/gnome/Shell",
        interface_name="org.gnome.Shell.Extensions",
        cancellable=None)
    shell_dbus.call_sync("InstallRemoteExtension",
                         GLib.Variant.new_tuple(GLib.Variant.new_string(extension_id)),
                         Gio.DBusCallFlags.NONE,
                         -1,
                         None)
