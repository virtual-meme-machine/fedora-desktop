#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  configure_system.sh                                                                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
#  Preforms the following actions:                                                                                     #
#   - Applies system settings via dconf                                                                                #
#   - Sets the default web browser to LibreWolf                                                                        #
#   - Deletes files and folders specified in the array below                                                           #
#   - Installs udev rules for the GameCube Controller Adapter for Wii U, this enables it for use with Dolphin          #
#   - Enables MangoHud globally and applies a default config file for it                                               #
########################################################################################################################

declare -A DCONF_VALUES=(
    ["/org/gnome/shell/extensions/ding/show-home"]="false"
    ["/org/gnome/shell/extensions/ding/show-trash"]="false"
)

declare -A GSETTINGS_VALUES=(
    # App picker layout settings
    ["org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/Utilities/ apps"]="['org.gnome.FileRoller.desktop', 'org.gnome.Calculator.desktop', 'org.gnome.Cheese.desktop', 'org.gnome.Connections.desktop', 'ca.desrt.dconf-editor.desktop', 'org.gnome.DiskUtility.desktop', 'org.gnome.baobab.desktop', 'simple-scan.desktop', 'org.gnome.Evince.desktop', 'org.fedoraproject.MediaWriter.desktop', 'org.gnome.font-viewer.desktop', 'yelp.desktop', 'org.gnome.eog.desktop', 'jetbrains-toolbox.desktop', 'nvidia-settings.desktop', 'org.freedesktop.GnomeAbrt.desktop', 'org.gnome.Settings.desktop', 'gnome-system-monitor.desktop', 'org.gnome.TextEditor.desktop', 'org.gnome.tweaks.desktop']"
    ["org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/Utilities/ name"]="Utilities"
    ["org.gnome.desktop.app-folders folder-children"]="['Games', 'Emulators', 'Utilities']"
    ["org.gnome.shell app-picker-layout"]="[{'Games': <{'position': <0>}>, 'Emulators': <{'position': <1>}>, 'Utilities': <{'position': <2>}>, 'org.gnome.Boxes.desktop': <{'position': <3>}>, 'com.mattjakeman.ExtensionManager.desktop': <{'position': <4>}>, 'org.filezillaproject.Filezilla.desktop': <{'position': <5>}>, 'org.freecadweb.FreeCAD.desktop': <{'position': <6>}>, 'org.gimp.GIMP.desktop': <{'position': <7>}>, 'io.github.benjamimgois.goverlay.desktop': <{'position': <8>}>, 'org.inkscape.Inkscape.desktop': <{'position': <9>}>, 'com.obsproject.Studio.desktop': <{'position': <10>}>, 'org.onlyoffice.desktopeditors.desktop': <{'position': <11>}>, 'net.davidotek.pupgui2.desktop': <{'position': <12>}>, 'com.prusa3d.PrusaSlicer.desktop': <{'position': <13>}>, 'com.prusa3d.PrusaSlicer.GCodeViewer.desktop': <{'position': <14>}>, 'org.qbittorrent.qBittorrent.desktop': <{'position': <15>}>, 'org.thentrythis.Samplebrain.desktop': <{'position': <16>}>, 'com.steamgriddb.SGDBoop.desktop': <{'position': <17>}>, 'com.steamgriddb.steam-rom-manager.desktop': <{'position': <18>}>, 'tiny-media-manager.desktop': <{'position': <19>}>, 'org.nickvision.tubeconverter.desktop': <{'position': <20>}>, 'com.github.Eloston.UngoogledChromium.desktop': <{'position': <21>}>, 'io.gitlab.azymohliad.WatchMate.desktop': <{'position': <22>}>}]"
    ["org.gnome.shell favorite-apps"]="['org.gnome.Nautilus.desktop', 'io.gitlab.librewolf-community.desktop', 'org.signal.Signal.desktop', 'org.jitsi.jitsi-meet.desktop', 'com.vscodium.codium.desktop', 'jetbrains-pycharm.desktop', 'jetbrains-rider.desktop', 'steam.desktop', 'com.spotify.Client.desktop', 'io.freetubeapp.FreeTube.desktop', 'org.videolan.VLC.desktop', 'org.gnome.Terminal.desktop', 'org.gnome.Software.desktop']"

    # Eye of Gnome (image viewer) settings
    ["org.gnome.eog.view extrapolate"]="false"
    ["org.gnome.eog.view interpolate"]="false"

    # Gnome Shell extension settings
    ["org.gnome.shell enabled-extensions"]="['appindicatorsupport@rgcjonas.gmail.com', 'blur-my-shell@aunetx', 'background-logo@fedorahosted.org', 'caffeine@patapon.info', 'ding@rastersoft.com', 'quick-settings-audio-panel@rayzeq.github.io']"
    ["org.fedorahosted.background-logo-extension logo-always-visible"]="true"
    ["org.fedorahosted.background-logo-extension logo-border"]="25"
    ["org.fedorahosted.background-logo-extension logo-opacity"]="20"
    ["org.fedorahosted.background-logo-extension logo-position"]="bottom-right"
    ["org.fedorahosted.background-logo-extension logo-size"]="5.0"

    # Nautilus (file manager) settings
    ["org.gnome.nautilus.preferences default-folder-viewer"]="list-view"
    ["org.gnome.nautilus.list-view default-zoom-level"]="small"
    ["org.gtk.gtk4.Settings.FileChooser sort-directories-first"]="true"
    ["org.gnome.nautilus.list-view use-tree-view"]="true"

    # System settings
    ["org.gnome.desktop.calendar show-weekdate"]="true"
    ["org.gnome.desktop.interface clock-format"]="12h"
    ["org.gnome.desktop.interface clock-show-weekday"]="true"
    ["org.gnome.desktop.interface color-scheme"]="prefer-dark"
    ["org.gnome.desktop.interface enable-hot-corners"]="false"
    ["org.gnome.desktop.interface gtk-theme"]="Adwaita-dark"
    ["org.gnome.desktop.media-handling autorun-never"]="true"
    ["org.gnome.desktop.privacy report-technical-problems"]="false"
    ["org.gnome.desktop.wm.preferences button-layout"]="appmenu:minimize,maximize,close"
    ["org.gnome.system.location enabled"]="false"
    ["org.gtk.Settings.FileChooser clock-format"]="12h"

    # Wallpaper settings
    ["org.gnome.desktop.background picture-uri"]="file:///usr/share/backgrounds/gnome/blobs-l.svg"
    ["org.gnome.desktop.background picture-uri-dark"]="file:///usr/share/backgrounds/gnome/blobs-d.svg"
    ["org.gnome.desktop.background primary-color"]="#241f31"
    ["org.gnome.desktop.screensaver picture-uri"]="file:///usr/share/backgrounds/gnome/blobs-l.svg"
    ["org.gnome.desktop.screensaver primary-color"]="#241f31"
)

DELETE_FOLDERS=(
    "$HOME/.cache/mozilla"
    "$HOME/.mozilla"
)

GC_ADAPTER_UDEV_FILE="/etc/udev/rules.d/51-gcadapter.rules"
GC_ADAPTER_UDEV_RULES="UBSYSTEM==\"usb\", ENV{DEVTYPE}==\"usb_device\", ATTRS{idVendor}==\"057e\", ATTRS{idProduct}==\"0337\", MODE=\"0666\""
MANGOHUD_CONFIG_DIR="/home/$USER/.config/MangoHud"
MANGOHUD_CONFIG_FILE="$MANGOHUD_CONFIG_DIR/MangoHud.conf"
MANGOHUD_ENABLED="MANGOHUD=1"
SYSTEM_ENVIRONMENT_FILE="/etc/environment"

# Add Emulators folder to app picker if user opted to install emulators
if [[ "$INSTALL_EMULATORS" == 0 ]]; then
    GSETTINGS_VALUES+=(
        ["org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/Emulators/ apps"]="['org.DolphinEmu.dolphin-emu.desktop', 'org.duckstation.DuckStation.desktop', 'io.mgba.mGBA.desktop', 'net.pcsx2.PCSX2.desktop', 'org.ppsspp.PPSSPP.desktop', 'app.xemu.xemu.desktop']"
        ["org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/Emulators/ name"]="Emulators"
    )
fi

# Add Games folder to app picker if user opted to install games
if [[ "$INSTALL_GAMES" == 0 ]]; then
    GSETTINGS_VALUES+=(
        ["org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/Games/ apps"]="['io.openrct2.OpenRCT2.desktop', 'org.polymc.PolyMC.desktop', 'org.sonic3air.Sonic3AIR.desktop', 'org.srb2.SRB2Kart.desktop', 'com.github.k4zmu2a.spacecadetpinball.desktop']"
        ["org.gnome.desktop.app-folders.folder:/org/gnome/desktop/app-folders/folders/Games/ name"]="Games"
    )
fi

# Set dconf values
print_header "Updating dconf values"
for key in "${!DCONF_VALUES[@]}"; do
    value=${DCONF_VALUES[$key]}
    echo "Setting dconf value: Key: '$key', Value: '$value'";
    if ! dconf write "$key" "$value"; then
        error_exit "Failed to set dconf value"
    fi
done
for key in "${!GSETTINGS_VALUES[@]}"; do
    value=${GSETTINGS_VALUES[$key]}
    echo "Setting dconf value: Key: '$key', Value: '$value'";
    if ! gsettings set $key "$value"; then
        error_exit "Failed to set dconf value"
    fi
done

# Set default web browser
print_header "Setting default web browser to LibreWolf"
if ! xdg-settings set default-web-browser io.gitlab.librewolf-community.desktop; then
    error_exit "Failed to set LibreWolf as default web browser"
else
    echo "Successfully set LibreWolf as default web browser"
fi

# Delete unused folders
print_header "Deleting unused folders"
for folder_path in ${DELETE_FOLDERS[*]}; do
    if [[ -d "$folder_path" ]]; then
        tput setaf 2
        echo "Deleting folder: $folder_path"
        tput sgr0

        if ! rm -rf "$folder_path"; then
            error_exit "Failed to delete folder: $folder_path"
        fi
    else
        echo "Folder '$folder_path' does not exist, skipping"
    fi
done

# Install udev rules for the GameCube Controller Adapter for Wii U
# Source: https://wiki.dolphin-emu.org/index.php?title=How_to_use_the_Official_GameCube_Controller_Adapter_for_Wii_U_in_Dolphin#Linux
if [[ ! -f "$GC_ADAPTER_UDEV_FILE" ]]; then
    print_header "Adding udev rules for the GameCube Controller Adapter for Wii U"
    echo "$GC_ADAPTER_UDEV_RULES" | sudo tee "$GC_ADAPTER_UDEV_FILE" &>/dev/null

    if ! less "$GC_ADAPTER_UDEV_FILE" | grep "$GC_ADAPTER_UDEV_RULES" &>/dev/null; then
        error_exit "Failed to add udev rules for the GameCube Controller Adapter for Wii U"
    else
        echo "Successfully added udev rules for the GameCube Controller Adapter for Wii U"
    fi
fi

# Enable MangoHud for all Vulkan applications
print_header "Enabling MangoHud"
if ! less "$SYSTEM_ENVIRONMENT_FILE" | grep "$MANGOHUD_ENABLED" &>/dev/null; then
    echo "$MANGOHUD_ENABLED" | sudo tee -a "$SYSTEM_ENVIRONMENT_FILE" &>/dev/null

    if ! less "$SYSTEM_ENVIRONMENT_FILE" | grep "$MANGOHUD_ENABLED" &>/dev/null; then
        error_exit "Failed to enable MangoHud globally"
    else
        echo "Successfully enabled MangoHud globally"
    fi
else
    echo "MangoHud already enabled globally"
fi

# Configure MangoHud
if [[ ! -f "$MANGOHUD_CONFIG_FILE" ]]; then
    echo "Creating a default MangoHud config file"

    # Create MangoHud config directory if needed
    if [[ ! -d "$MANGOHUD_CONFIG_DIR" ]]; then
        if ! mkdir -p "$MANGOHUD_CONFIG_DIR"; then
            error_exit "Failed to create MangoHud config directory '$MANGOHUD_CONFIG_DIR'"
        fi
    fi

    # Create MangoHud config file
    cat > "$MANGOHUD_CONFIG_FILE" <<- EOF
		# Overlay layout
		legacy_layout=false
		gpu_stats
		gpu_temp
		gpu_load_change
		gpu_load_value=50,90
		gpu_load_color=FFFFFF,FFAA7F,CC0000
		gpu_text=GPU
		cpu_stats
		cpu_temp
		cpu_load_change
		core_load_change
		cpu_load_value=50,90
		cpu_load_color=FFFFFF,FFAA7F,CC0000
		cpu_color=2e97cb
		cpu_text=CPU
		io_color=a491d3
		vram
		vram_color=ad64c1
		ram
		ram_color=c26693
		fps
		engine_color=eb5b5b
		gpu_color=2e9762
		wine_color=eb5b5b
		frame_timing=1
		frametime_color=00ff00
		media_player_color=ffffff
		background_alpha=0.2
		font_size=24

		# Overlay position and style
		background_color=020202
		position=top-left
		text_color=ffffff
		round_corners=5

		# Key Bindings
		upload_log=Shift_R+F10
		toggle_logging=Shift_R+F11
		toggle_hud=Shift_R+F12
	EOF
fi

exit 0
