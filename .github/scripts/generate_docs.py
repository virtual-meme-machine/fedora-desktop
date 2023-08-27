#!/usr/bin/env python3

import json
import os
import sys

__PACKAGE_ROOT: str = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
sys.path.append(os.path.join(__PACKAGE_ROOT, "src"))

from data.Paths import DOCS_DIR, OPTIONS_DIR
from data.Category import Category, from_string

CATEGORY_LISTS: dict[Category, list[str]] = {}


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


def main():
    """
    Generates documentation for the package
    :param package_root: Path to the root of this package
    :return: None
    """
    options_doc: str = os.path.join(DOCS_DIR, "Options.md")

    if not os.path.isdir(OPTIONS_DIR):
        raise NotADirectoryError(f"Options directory '{OPTIONS_DIR}' is not a directory")

    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)

    for option_file in os.listdir(OPTIONS_DIR):
        if not os.path.splitext(option_file)[1] == ".json":
            continue

        with open(os.path.join(OPTIONS_DIR, option_file), "r") as json_file:
            for option in json.load(json_file):
                category = from_string(option.get("category"))
                value_list = ([], CATEGORY_LISTS.get(category))[category in CATEGORY_LISTS.keys()]
                value_list.append(get_option_string(option))
                CATEGORY_LISTS.update({category: value_list})

    print(f"Generating documentation...")
    with open(options_doc, "w") as file:
        print(f"Writing file: '{options_doc}'")
        file.write("# Fedora Desktop Configurator - Options\n\n")
        for category in sorted(CATEGORY_LISTS, key=lambda c: c.value[0]):
            file.write(f"## {category.value[1]}\n\n")
            file.write(f"| Option | Description | Link |\n")
            file.write(f"| ------ | ----------- | ---- |\n")
            for line in sorted(CATEGORY_LISTS.get(category), key=lambda o: o.replace("[", "").lower()):
                file.write(f"{line}\n")

            file.write("\n")


if __name__ == "__main__":
    main()
