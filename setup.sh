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
./scripts/install_packages.sh

# Install Flatpak applications
./scripts/install_flatpaks.sh

# Install Gnome Shell extensions
./scripts/install_extensions.sh

# Configure system
./scripts/configure_system.sh

# Configure and enable VPN
./scripts/configure_vpn.sh

# Print setup complete message
print_header "Setup Complete"
echo "You will need to reboot the host in order for most changes to take effect."
echo "Enjoy!"

exit 0
