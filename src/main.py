#!/usr/bin/env python3

import platform
import sys

from gui.AdwApp import AdwApp
from utils.platform_utils import get_fedora_version

APPLICATION_ID: str = "com.meme.fedora.desktop.configurator"
SUPPORTED_FEDORA_VERSIONS: list[int] = [37, 38]

if __name__ == "__main__":
    operating_system = platform.system()
    if operating_system != "Linux":
        print(f"This script does not support OS: {operating_system}")
        exit(200)

    distro = platform.freedesktop_os_release().get("NAME")
    if distro != "Fedora Linux":
        print(f"This script does not support Linux distro: {distro}")
        exit(201)

    variant = platform.freedesktop_os_release().get("VARIANT_ID")
    if variant != "workstation":
        print(f"This script does not support Fedora variant: {variant}")
        exit(202)

    version = get_fedora_version()
    if version not in SUPPORTED_FEDORA_VERSIONS:
        print(f"This script does not support Fedora version: {version}")
        exit(203)

    adw_app = AdwApp(application_id=APPLICATION_ID)
    adw_app.run(sys.argv)
