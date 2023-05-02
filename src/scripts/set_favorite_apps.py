from utils.platform_utils import get_gsettings_json, is_application_installed, set_gsettings_json

FAVORITE_APPS: list[str] = [
    "org.gnome.Nautilus.desktop",
    "io.gitlab.librewolf-community.desktop",
    "org.signal.Signal.desktop",
    "org.jitsi.jitsi-meet.desktop",
    "com.vscodium.codium.desktop",
    "jetbrains-pycharm.desktop",
    "jetbrains-rider.desktop",
    "steam.desktop",
    "com.spotify.Client.desktop",
    "io.freetubeapp.FreeTube.desktop",
    "org.videolan.VLC.desktop",
    "org.gnome.Terminal.desktop",
    "org.gnome.Software.desktop"
]


def execute():
    """
    Sets the applications pinned to the dash to a preconfigured layout
    :return: None
    """
    installed_applications = []

    for app in FAVORITE_APPS:
        if is_application_installed(app):
            installed_applications.append(app)

    if not installed_applications:
        print("Nothing to do")
        return

    if get_gsettings_json(schema="org.gnome.shell", key="favorite-apps") == installed_applications:
        print("Favorite applications already set")
        return

    set_gsettings_json(schema="org.gnome.shell", key="favorite-apps", value=installed_applications)
