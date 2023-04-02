#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  install_flatpaks.sh                                                                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
#  Preforms the following actions:                                                                                     #
#   - Verifies Flatpak is installed                                                                                    #
#   - Removes Fedora Flatpak repos                                                                                     #
#   - Adds Flathub Flatpak repo                                                                                        #
#   - Installs Flatpaks specified in the array below                                                                   #
########################################################################################################################

APPLICATION_IDS=(
    org.filezillaproject.Filezilla              # FileZilla
    io.freetubeapp.FreeTube                     # FreeTube
    org.gnome.Boxes                             # Gnome Boxes
    com.mattjakeman.ExtensionManager            # Gnome Extension Manager
    org.gimp.GIMP                               # GNU Image Manipulation Program
    org.inkscape.Inkscape                       # Inkscape
    org.jitsi.jitsi-meet                        # Jitsi Meet
    io.gitlab.librewolf-community               # LibreWolf
    org.onlyoffice.desktopeditors               # OnlyOffice Desktop Editors
    net.davidotek.pupgui2                       # ProtonUp-Qt (Proton Updater)
    com.prusa3d.PrusaSlicer                     # PrusaSlicer
    org.qbittorrent.qBittorrent                 # qBittorrent
    org.thentrythis.Samplebrain                 # Samplebrain (Aphex Twin)
    org.signal.Signal                           # Signal Desktop
    com.spotify.Client                          # Spotify
    com.steamgriddb.SGDBoop                     # SGDBoop
    com.steamgriddb.steam-rom-manager           # Steam ROM Manager
    org.nickvision.tubeconverter                # Tube Converter
    com.github.Eloston.UngoogledChromium        # UnGoogled Chromium
    org.videolan.VLC                            # VLC Media Player
    com.vscodium.codium                         # VSCodium
    io.gitlab.azymohliad.WatchMate              # WatchMate (PineTime Sync)
)

# Add emulator flatpak IDs if user opted to install emulators
if [[ "$INSTALL_EMULATORS" == 0 ]]; then
    APPLICATION_IDS+=(
        org.DolphinEmu.dolphin-emu              # Dolphin Emulator, Gamecube and Wii emulator
        org.duckstation.DuckStation             # DuckStation, PS1 emulator
        io.mgba.mGBA                            # mGBA, GameBoy Advance emulator
        net.pcsx2.PCSX2                         # PCSX2, PS2 emulator
        org.ppsspp.PPSSPP                       # PPSSPP, PSP emulator
        app.xemu.xemu                           # Xemu, Xbox Emulator
    )
fi

# Add game flatpak IDs if user opted to install games
if [[ "$INSTALL_GAMES" == 0 ]]; then
    APPLICATION_IDS+=(
        io.openrct2.OpenRCT2                    # OpenRCT2
        org.polymc.PolyMC                       # PolyMC Minecraft Launcher
        org.sonic3air.Sonic3AIR                 # Sonic 3: Angel Island Revisited
        org.srb2.SRB2Kart                       # Sonic Robo Blast 2 Kart
        com.github.k4zmu2a.spacecadetpinball    # Space Cadet Pinball
    )
fi

# Verify Flatpak is installed and available
exec_exists "flatpak"

# Remove Fedora Flatpak repos
print_header "Removing Fedora Flatpak repos"
flatpak remote-delete fedora --force &>/dev/null
flatpak remote-delete fedora-testing --force &>/dev/null

# Verify Fedora Flatpak repos were removed
if flatpak remotes | grep fedora &>/dev/null; then
    error_exit "Failed to remove Fedora Flatpak repos"
else
    echo "Successfully removed Fedora Flatpak repos"
fi

# Add Flathub repo
print_header "Adding Flathub Flatpak repo"
flatpak remote-delete flathub --force &>/dev/null
if ! flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo; then
    error_exit "Failed to add Flathub Flatpak repo"
fi

# Verify Flathub repo was added
if ! flatpak remotes | grep flathub &>/dev/null; then
    error_exit "Failed to add Flathub Flatpak repo"
else
    echo "Successfully added Flathub Flatpak repo"
fi

# Install Flatpak applications
print_header "Installing Flatpak applications"
for flatpak_id in ${APPLICATION_IDS[*]}; do
    tput setaf 2
    echo "Installing Flatpak: $flatpak_id"
    tput sgr0

    if ! flatpak install flathub --noninteractive "$flatpak_id"; then
        error_exit "Failed to install Flatpak: $flatpak_id"
    fi
done

exit 0
