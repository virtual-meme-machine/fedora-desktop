#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  install_packages.sh                                                                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
#  Preforms the following actions:                                                                                     #
#   - Removes packages specified in the array below                                                                    #
#   - Adds RPM Fusion repos                                                                                            #
#   - Installs available updates                                                                                       #
#   - Installs packages specified in the array below                                                                   #
#   - Creates a .desktop file for TinyMediaManager if installed                                                        #
########################################################################################################################

INSTALL_PACKAGES=(
    akmod-nvidia                                # Drivers for modern Nvidia GPUs
    dconf-editor                                # GUI for viewing and modifying dconf
    gnome-tweaks                                # Gnome Tweaks, required to configure some Gnome settings
    goverlay                                    # Configures in game performance monitoring overlays
    file-roller                                 # Gnome Archive Manager
    libmediainfo                                # Required by TinyMediaManager
    mangohud                                    # In game performance monitoring overlay similar to MSI Afterburner
    steam                                       # Steam
    steam-devices                               # Udev rules for HID devices recognized by Steam such as controllers
    unrar                                       # Allows the system to extract .rar archives
    wireguard-tools                             # Wireguard configuration utilities, used by most modern VPNs
    xorg-x11-drv-nvidia-cuda                    # Libraries for Nvidia CUDA
)

REMOVE_PACKAGES=(
    firefox                                     # Firefox
    gnome-calendar                              # Gnome Calendar
    gnome-characters                            # Gnome Characters
    gnome-clocks                                # Gnome Clocks
    gnome-contacts                              # Gnome Contacts
    gnome-logs                                  # Gnome Logs
    gnome-maps                                  # Gnome Maps
    gnome-music                                 # Gnome Music
    gnome-photos                                # Gnome Photos
    gnome-weather                               # Gnome Weather
    totem                                       # Gnome Videos
    rhythmbox                                   # Rhythmbox, music manager similar to iTunes
    gnome-tour                                  # Gnome Tour
)

TINY_MEDIA_MANAGER_DESKTOP="/home/$USER/.local/share/applications/tiny-media-manager.desktop"
TINY_MEDIA_MANAGER_EXEC="/home/$USER/.var/app/tinyMediaManager/tinyMediaManager"
TINY_MEDIA_MANAGER_ICON="/home/$USER/.var/app/tinyMediaManager/tmm.png"

# Remove unwanted default packages
print_header "Removing unwanted default packages"
for package_name in ${REMOVE_PACKAGES[*]}; do
    tput setaf 2
    echo "Removing package: $package_name"
    tput sgr0

    if ! sudo dnf -y remove "$package_name"; then
        error_exit "Failed to remove package: $package_name"
    fi
done

# Remove all LibreOffice packages
tput setaf 2
echo "Removing LibreOffice"
tput sgr0

if ! sudo dnf -y remove libreoffice*; then
    error_exit "Failed to remove LibreOffice"
fi

# Auto remove unneeded dependencies
if ! sudo dnf -y autoremove; then
    error_exit "Failed to remove unused dependencies"
fi

# Add RPM Fusion repos
print_header "Enabling RPM Fusion repos"
if ! sudo dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm; then
    error_exit "Failed to enable RPM Fusion free repo"
fi

if ! sudo dnf -y install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm; then
    error_exit "Failed to enable RPM Fusion non-free repo"
fi

# Install any available updates
print_header "Installing updates"
if ! sudo dnf -y update --refresh; then
    error_exit "Failed to install updates"
fi

# Install packages
print_header "Installing packages"
for package_name in ${INSTALL_PACKAGES[*]}; do
    tput setaf 2
    echo "Installing package: $package_name"
    tput sgr0

    if ! sudo dnf -y install "$package_name"; then
        error_exit "Failed to install package: $package_name"
    fi
done

# If TinyMediaManager is found, create a .desktop for it
if [[ -f "$TINY_MEDIA_MANAGER_EXEC" ]] && [[ ! -f "$TINY_MEDIA_MANAGER_DESKTOP" ]]; then
    echo "Creating a .desktop for TinyMediaManager at '$TINY_MEDIA_MANAGER_DESKTOP'"
    cat > "$TINY_MEDIA_MANAGER_DESKTOP" <<- EOF
		[Desktop Entry]
		Type=Application
		Terminal=false
		Name=TinyMediaManager
		Icon=$TINY_MEDIA_MANAGER_ICON
		Exec=$TINY_MEDIA_MANAGER_EXEC
	EOF
fi

exit 0
