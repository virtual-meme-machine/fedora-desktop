import dbus

from data.Info import APPLICATION_NAME

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


def activate_caffeine() -> dbus.UInt32:
    """
    Activates a new caffeine session
    :return: Integer that is used to track the caffeine session
    """
    inhibit_method = getattr(__get_interface(), METHOD_NAME_INHIBIT)
    caffeine_cookie = inhibit_method(APPLICATION_NAME, 0, APPLICATION_NAME, 8)
    print(f"Started caffeine session: {caffeine_cookie}")
    return caffeine_cookie


def deactivate_caffeine(caffeine_cookie: dbus.UInt32):
    """
    Deactivates a given caffeine session
    :param caffeine_cookie: Integer for the caffeine session we want to deactivate
    :return: None
    """
    un_inhibit_method = getattr(__get_interface(), METHOD_NAME_UN_INHIBIT)
    un_inhibit_method(caffeine_cookie)
    print(f"Ended caffeine session: {caffeine_cookie}")
