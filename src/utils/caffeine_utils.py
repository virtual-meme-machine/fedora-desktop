import dbus

from data.Info import APPLICATION_NAME

CAFFEINE_COOKIE: dbus.UInt32 or None = None
INTERFACE_NAME: str = "org.gnome.SessionManager"
INTERFACE_PATH: str = "/org/gnome/SessionManager"
METHOD_NAME_INHIBIT: str = "Inhibit"
METHOD_NAME_UN_INHIBIT: str = "Uninhibit"


def __get_interface() -> dbus.Interface:
    """
    Generates a new Gnome SessionManager D-Bus interface
    :return: D-Bus interface for sending 'inhibit' commands to Gnome SessionManager
    """
    bus = dbus.SessionBus()
    dbus_object = bus.get_object(INTERFACE_NAME, INTERFACE_PATH)
    return dbus.Interface(dbus_object, INTERFACE_NAME)


def activate_caffeine():
    """
    Activates a new caffeine session
    :return: None
    """
    global CAFFEINE_COOKIE
    if CAFFEINE_COOKIE is not None:
        return

    inhibit_method = getattr(__get_interface(), METHOD_NAME_INHIBIT)
    caffeine_cookie = inhibit_method(APPLICATION_NAME, 0, APPLICATION_NAME, 8)
    print(f"Started caffeine session: {caffeine_cookie}")

    CAFFEINE_COOKIE = caffeine_cookie


def deactivate_caffeine():
    """
    Deactivates the current caffeine session
    :return: None
    """
    global CAFFEINE_COOKIE
    if CAFFEINE_COOKIE is None:
        return

    un_inhibit_method = getattr(__get_interface(), METHOD_NAME_UN_INHIBIT)
    un_inhibit_method(CAFFEINE_COOKIE)
    print(f"Ended caffeine session: {CAFFEINE_COOKIE}")

    CAFFEINE_COOKIE = None


def deactivate_caffeine_exit(exit_code: int = 1):
    """
    Deactivates caffeine and exits, this should only be used for handling fatal errors
    :param exit_code: Exit code to return
    :return: None
    """
    deactivate_caffeine()
    exit(exit_code)
