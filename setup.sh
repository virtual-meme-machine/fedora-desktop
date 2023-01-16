#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  setup.sh                                                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
#  Main script that handles kicking off sub-scripts in this package.                                                   #
########################################################################################################################

SCRIPT_VERSION="2.0-$(git rev-parse --short HEAD)"

# Print initial splash header
clear
print_header "Fedora Workstation Configurator - Version $SCRIPT_VERSION"
echo "Welcome! This script is mostly automated but you will be prompted for authentication several times."
sleep 2

# Install packages
if ! ./scripts/install_packages.sh; then
    exit 1
fi

# Install Flatpak applications
if ! ./scripts/install_flatpaks.sh; then
    exit 1
fi

# Install JetBrains Toolbox
if ! ./scripts/install_toolbox.sh; then
    exit 1
fi

# Install Gnome Shell extensions
if ! ./scripts/install_extensions.sh; then
    exit 1
fi

# Configure system
if ! ./scripts/configure_system.sh; then
    exit 1
fi

# Configure and enable VPN
if ! ./scripts/configure_vpn.sh; then
    exit 1
fi

# Print setup complete message
print_header "Setup Complete"
echo "You will need to reboot the host in order for most changes to take effect."
echo "Enjoy!"

exit 0
