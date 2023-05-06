#!/usr/bin/env python3

import json
import os
import sys

CATEGORY_LISTS: dict[str, list[str]] = {}
HEADER_CATEGORIES: dict[str, str] = {
    "application": "Install Applications",
    "emulator": "Install Emulators",
    "game": "Install Games",
    "gnome_extension": "Install Gnome Shell Extensions",
    "setting": "Configure Settings",
    "system": "Configure System"
}
OPTION_URLS: dict[str, str] = {
    "blur-my-shell@aunetx": "https://extensions.gnome.org/extension/3193/blur-my-shell",
    "caffeine@patapon.info": "https://extensions.gnome.org/extension/517/caffeine",
    "configure_mangohud": "https://github.com/virtual-meme-machine/fedora-desktop#mangohud",
    "configure_mullvad_vpn": "https://mullvad.net",
    "ding@rastersoft.com": "https://extensions.gnome.org/extension/2087/desktop-icons-ng-ding",
    "enable_gc_adapter": "https://wiki.dolphin-emu.org/index.php?title=How_to_use_the_Official_GameCube_Controller_Adapter_for_Wii_U_in_Dolphin#Linux",
    "install_tiny_media_manager": "https://www.tinymediamanager.org",
    "install_toolbox": "https://www.jetbrains.com/toolbox-app"
}


def get_option_string(option: dict[str, str]) -> str:
    """
    Gets a nicely formatted string for an option
    :param option: Dictionary containing data about a single option
    :return: Nicely formatted string for an option, may contain a link
    """
    name = option.get("name")
    operation_type = option.get("operation_type")
    operation_args = option.get("operation_args")
    if operation_type == "flatpak":
        return f"[{name}](https://flathub.org/apps/{operation_args[0]})"
    elif operation_type == "package_install":
        return f"[{name}](https://packages.fedoraproject.org/pkgs/{operation_args[0]}/{operation_args[0]})"
    elif operation_type == "package_install_rpmfusion":
        return f"[{name}](https://admin.rpmfusion.org/pkgdb/package/nonfree/{operation_args[0]})"
    elif type(operation_args[0]) is str:
        if operation_args[0] in OPTION_URLS.keys():
            return f"[{name}]({OPTION_URLS.get(operation_args[0])})"

    return name


def main(package_root: str):
    """
    Generates documentation for the package
    :param package_root: Path to the root of this package
    :return: None
    """
    docs_dir: str = os.path.join(package_root, "docs")
    output_file: str = os.path.join(docs_dir, "Options.md")
    resources_dir: str = os.path.join(package_root, "resources")

    if not os.path.isdir(package_root):
        raise NotADirectoryError(f"Provided package root '{package_root}' is not a directory")

    if not os.path.isdir(resources_dir):
        raise NotADirectoryError(f"Resources directory '{resources_dir}' is not a directory")

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    for option_file in os.listdir(resources_dir):
        if not os.path.splitext(option_file)[1] == ".json":
            continue

        with open(os.path.join(resources_dir, option_file), "r") as json_file:
            for option in json.load(json_file):
                key = HEADER_CATEGORIES.get(option.get("category"))
                value_list = []
                if key in CATEGORY_LISTS.keys():
                    value_list = CATEGORY_LISTS.get(key)

                value_list.append(get_option_string(option))
                CATEGORY_LISTS.update({key: value_list})

    print(f"Generating documentation...")
    with open(output_file, "w") as file:
        print(f"Writing file: '{output_file}'")
        file.write("# Fedora Desktop Configurator - Options\n\n")
        for key in CATEGORY_LISTS:
            file.write(f"## {key}\n\n")
            for line in sorted(CATEGORY_LISTS.get(key), key=lambda o: o.replace("[", "").lower()):
                file.write(f"- {line}\n")

            file.write("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: '{sys.argv[0]} $path_to_package_root'")
        exit(1)

    main(sys.argv[1])
