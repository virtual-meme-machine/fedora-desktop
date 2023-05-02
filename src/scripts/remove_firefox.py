import os

import utils.dnf_utils as dnf_utils
import utils.file_utils as file_utils

REMOVE_PATHS = [
    os.path.expanduser("~/.cache/mozilla"),
    os.path.expanduser("~/.mozilla")
]


def execute():
    """
    Uninstalls Mozilla Firefox
    :return: None
    """
    dnf_utils.remove_packages(["firefox"])

    for path in REMOVE_PATHS:
        file_utils.delete_path(path)
