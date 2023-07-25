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
    "system": "Configure System",
    "vpn": "Configure VPN"
}


def get_option_string(option: dict[str, str]) -> str:
    """
    Gets a nicely formatted string for an option
    :param option: Dictionary containing data about a single option
    :return: Nicely formatted string for an option, may contain a link
    """
    name = option.get("name")
    description = option.get("description")
    link = option.get("documentation_link")
    operation_type = option.get("operation_type")
    operation_args = option.get("operation_args")

    if link is None:
        if operation_type == "flatpak":
            link = f"[View on Flathub](https://flathub.org/apps/{operation_args[0]})"
        elif operation_type == "package_install":
            link = f"[View on Fedora Packages](https://packages.fedoraproject.org/pkgs/" \
                   f"{operation_args[0]}/{operation_args[0]})"
        elif operation_type == "package_install_rpmfusion":
            link = f"[View on RPM Fusion](https://admin.rpmfusion.org/pkgdb/package/nonfree/{operation_args[0]})"
        else:
            link = "N/A"

    return f"| {name} | {description} | {link} |"


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
        for key in sorted(CATEGORY_LISTS, key=lambda c: c.replace("Install ", "").replace("Configure ", "").lower()):
            file.write(f"## {key}\n\n")
            file.write(f"| Option | Description | Link |\n")
            file.write(f"| ------ | ----------- | ---- |\n")
            for line in sorted(CATEGORY_LISTS.get(key), key=lambda o: o.replace("[", "").lower()):
                file.write(f"{line}\n")

            file.write("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: '{sys.argv[0]} $path_to_package_root'")
        exit(1)

    main(sys.argv[1])
