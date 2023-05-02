from enum import Enum


class OperationType(Enum):
    """
    Types of operation that can be preformed to configure the system
    """
    FLATPAK: str = "flatpak"
    GNOME_EXTENSION: str = "gnome_extension"
    GSETTINGS_VALUE: str = "gsettings_value"
    PACKAGE_INSTALL: str = "package_install"
    PACKAGE_INSTALL_RPMFUSION: str = "package_install_rpmfusion"
    PACKAGE_REMOVE: str = "package_remove"
    SCRIPT: str = "script"


def from_string(string: str) -> OperationType:
    """
    Gets an OperationType from the provided input
    :param string: String that we want to get an OperationType value for
    :return: Corresponding OperationType value
    """
    for operation_type in OperationType:
        if operation_type.value == string:
            return operation_type

    raise ValueError(f"Invalid OperationType: '{string}'")
