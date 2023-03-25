#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  setup.sh                                                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
#  Main script that handles kicking off sub-scripts in this package.                                                   #
########################################################################################################################

SCRIPT_VERSION="2.1-$(git rev-parse --short HEAD)"

# Set pipe fail
set -e

# Print initial splash header
clear
print_header "Fedora Workstation Configurator - Version $SCRIPT_VERSION"
echo "Welcome! This script is mostly automated but you will be prompted for authentication several times."
echo "Select the package groups you would like to install:"

# Prompt for installation options
INSTALL_NVIDIA_DRIVERS=$(prompt_yes_no "  [1/5] Install Nvidia drivers?"); export INSTALL_NVIDIA_DRIVERS
INSTALL_VPN=$(prompt_yes_no "  [2/5] Install Mullvad VPN via Wireguard?"); export INSTALL_VPN
INSTALL_TOOLBOX=$(prompt_yes_no "  [3/5] Install JetBrains Toolbox (eg: PyCharm, IntelliJ)?"); export INSTALL_TOOLBOX
INSTALL_EMULATORS=$(prompt_yes_no "  [4/5] Install Emulators (eg: Dolphin, mGBA)?"); export INSTALL_EMULATORS
INSTALL_GAMES=$(prompt_yes_no "  [5/5] Install Games (eg: OpenRCT2, Minecraft Launcher)?"); export INSTALL_GAMES

# Run install and configure scripts
echo "Starting setup in 3 seconds..."
sleep 3

./scripts/install_packages.sh
./scripts/install_flatpaks.sh
./scripts/install_toolbox.sh
./scripts/install_extensions.sh
./scripts/configure_system.sh
./scripts/configure_vpn.sh

# Print setup complete message
print_header "Setup Complete"
echo "You will need to reboot the host in order for most changes to take effect."
echo "Enjoy!"

exit 0
