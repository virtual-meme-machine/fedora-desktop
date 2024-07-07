import time

from utils.platform_utils import get_application_name, get_application_categories, get_gsettings_json, \
    get_gsettings_value, get_installed_applications, set_gsettings_json, set_gsettings_value

UTILITIES_FOLDER: list[str] = [
    "ca.desrt.dconf-editor.desktop",
    "com.mattjakeman.ExtensionManager.desktop",
    "com.steamgriddb.SGDBoop.desktop",
    "fr.romainvigier.MetadataCleaner.desktop",
    "gnome-system-monitor.desktop",
    "io.github.benjamimgois.goverlay.desktop",
    "jetbrains-toolbox.desktop",
    "net.davidotek.pupgui2.desktop",
    "nvidia-settings.desktop",
    "org.fedoraproject.MediaWriter.desktop",
    "org.freedesktop.GnomeAbrt.desktop",
    "org.gnome.baobab.desktop",
    "org.gnome.Calculator.desktop",
    "org.gnome.Cheese.desktop",
    "org.gnome.Connections.desktop",
    "org.gnome.DiskUtility.desktop",
    "org.gnome.eog.desktop",
    "org.gnome.Loupe.desktop",
    "org.gnome.Evince.desktop",
    "org.gnome.FileRoller.desktop",
    "org.gnome.font-viewer.desktop",
    "org.gnome.Settings.desktop",
    "org.gnome.SystemMonitor.desktop",
    "org.gnome.TextEditor.desktop",
    "org.gnome.tweaks.desktop",
    "simple-scan.desktop",
    "yelp.desktop"
]


def __alphabetize_applications(application_list: list[str]) -> list[str]:
    """
    Sorts a list of application .desktop files alphabetically by the application name
    :param application_list: List of application .desktop files that we want to sort
    :return: List of application .desktop files sorted alphabetically, applications that could not be found are skipped
    """
    application_dict = {}
    for app_id in application_list:
        app_name = get_application_name(app_id)
        if app_name is not None:
            application_dict.update({app_name.lower(): app_id})

    return list(dict(sorted(application_dict.items())).values())


def __create_folder(name: str, application_list: list[str]):
    """
    Creates a new folder in the app picker
    :param name: Name of the folder we want to create
    :param application_list: List of application .desktops to be added to the folder
    :return: None
    """
    installed_applications = __alphabetize_applications(application_list)

    if not installed_applications:
        print(f"No specified applications are installed, unable to create folder '{name}'")
        return

    schema = f"org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/{name}/"
    set_gsettings_json(schema=schema, key="apps", value=installed_applications)
    set_gsettings_value(schema=schema, key="name", value=f"'{name}'")

    folder_list = __get_folder_list()
    if name not in folder_list:
        __set_folder_list(folder_list + [name])


def __get_folder_list() -> list[str]:
    """
    Gets the list of folders in the app picker
    :return: List of folder names
    """
    return get_gsettings_json(schema="org.gnome.desktop.app-folders", key="folder-children")


def __set_folder_list(folder_list: list[str]):
    """
    Sets the list of folders in the app picker
    :param folder_list:
    :return: None
    """
    return set_gsettings_json(schema="org.gnome.desktop.app-folders", key="folder-children", value=folder_list)


def execute():
    """
    Arranges the app picker to a preconfigured layout
    :return: None
    """
    applications = []
    emulators = []
    games = []

    application_list = get_installed_applications()
    for app in application_list:
        if app in UTILITIES_FOLDER:
            continue

        app_categories = get_application_categories(app)
        if app_categories is None:
            continue
        elif "Game" in app_categories and "Emulator" in app_categories:
            emulators.append(app)
        elif "Game" in app_categories:
            games.append(app)
        else:
            applications.append(app)

    __create_folder("Emulators", emulators)
    __create_folder("Games", games)
    __create_folder("Utilities", UTILITIES_FOLDER)

    app_picker_list = sorted(__get_folder_list()) + __alphabetize_applications(applications)
    if not app_picker_list:
        print("No specified applications are installed, unable to set app picker layout")
        return

    position_counter = 0
    app_position_list = []
    for app in app_picker_list:
        app_position_list.append(f"'{app}': <{{'position': <{position_counter}>}}>")
        position_counter += 1

    app_picker_string = f"[{{{', '.join(app_position_list)}}}]"
    if get_gsettings_value(schema="org.gnome.shell", key="app-picker-layout") == app_picker_string:
        print("App picker layout already set")
        return

    # We apply this 3 times because it doesn't always stick on the first try
    for i in range(3):
        set_gsettings_value(schema="org.gnome.shell",
                            key="app-picker-layout",
                            value=app_picker_string)
        time.sleep(1)
