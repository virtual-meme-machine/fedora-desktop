import time

from utils.platform_utils import get_gsettings_json, get_gsettings_value, is_application_installed, set_gsettings_json, \
    set_gsettings_value

FOLDERS: dict[str, list[str]] = {
    "Emulators": [
        "org.DolphinEmu.dolphin-emu.desktop",
        "org.duckstation.DuckStation.desktop",
        "io.mgba.mGBA.desktop",
        "net.pcsx2.PCSX2.desktop",
        "org.ppsspp.PPSSPP.desktop",
        "org.ryujinx.Ryujinx.desktop",
        "app.xemu.xemu.desktop"
    ],
    "Games": [
        "com.github.Anuken.Mindustry.desktop",
        "io.openrct2.OpenRCT2.desktop",
        "org.polymc.PolyMC.desktop",
        "org.sonic3air.Sonic3AIR.desktop",
        "org.srb2.SRB2Kart.desktop",
        "com.github.k4zmu2a.spacecadetpinball.desktop"
    ],
    "Utilities": [
        "org.gnome.FileRoller.desktop",
        "org.gnome.Calculator.desktop",
        "org.gnome.Cheese.desktop",
        "org.gnome.Connections.desktop",
        "ca.desrt.dconf-editor.desktop",
        "org.gnome.DiskUtility.desktop",
        "org.gnome.baobab.desktop",
        "simple-scan.desktop",
        "org.gnome.Evince.desktop",
        "com.mattjakeman.ExtensionManager.desktop",
        "org.fedoraproject.MediaWriter.desktop",
        "org.gnome.font-viewer.desktop",
        "io.github.benjamimgois.goverlay.desktop",
        "yelp.desktop",
        "org.gnome.eog.desktop",
        "jetbrains-toolbox.desktop",
        "fr.romainvigier.MetadataCleaner.desktop",
        "nvidia-settings.desktop",
        "org.freedesktop.GnomeAbrt.desktop",
        "net.davidotek.pupgui2.desktop",
        "org.gnome.Settings.desktop",
        "com.steamgriddb.SGDBoop.desktop",
        "gnome-system-monitor.desktop",
        "org.gnome.TextEditor.desktop",
        "org.gnome.tweaks.desktop"
    ]
}
LAYOUT: list[str] = [
    "org.gnome.Boxes.desktop",
    "org.filezillaproject.Filezilla.desktop",
    "org.freecadweb.FreeCAD.desktop",
    "org.gimp.GIMP.desktop",
    "org.inkscape.Inkscape.desktop",
    "com.obsproject.Studio.desktop",
    "org.onlyoffice.desktopeditors.desktop",
    "org.openrgb.OpenRGB.desktop",
    "com.prusa3d.PrusaSlicer.desktop",
    "com.prusa3d.PrusaSlicer.GCodeViewer.desktop",
    "org.qbittorrent.qBittorrent.desktop",
    "org.thentrythis.Samplebrain.desktop",
    "com.steamgriddb.steam-rom-manager.desktop",
    "tiny-media-manager.desktop",
    "org.nickvision.tubeconverter.desktop",
    "com.github.Eloston.UngoogledChromium.desktop",
    "io.gitlab.azymohliad.WatchMate.desktop"
]


def __create_folder(name: str, contents: list[str]):
    """
    Creates a new folder in the app picker
    :param name: Name of the folder we want to create
    :param contents: List of application .desktops to be added to the folder
    :return: None
    """
    installed_applications = []

    for app in contents:
        if is_application_installed(app):
            installed_applications.append(app)

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
    for folder_name in FOLDERS.keys():
        __create_folder(name=folder_name, contents=FOLDERS.get(folder_name))

    app_picker_list = sorted(__get_folder_list())
    for app in LAYOUT:
        if is_application_installed(app):
            app_picker_list.append(app)

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
