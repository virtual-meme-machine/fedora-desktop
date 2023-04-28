# fedora-desktop

This package contains a set of scripts designed to configure a clean installation of Fedora Workstation.

Supports Fedora Workstation 38 (GNOME) as of April 2023, older versions of this script support Fedora 37.

![image](https://user-images.githubusercontent.com/46010615/235053773-0e3e8187-b2a6-4347-a583-d0f6c4ec0603.png)


## Usage

**!! DO NOT enable third-party repos if asked, this script will set up RPM Fusion and Flathub on its own !!**

1. Clean install [Fedora Workstation](https://getfedora.org/en/workstation) on your host
2. Preform initial setup (creating an account, etc.)
3. Once at the desktop, open a terminal and git clone this package somewhere on the host:
    ```none
    git clone https://github.com/virtual-meme-machine/fedora-desktop.git ~/fedora-desktop
    ```
4. Enter the package directory and run `setup.sh`:
    ```none
    cd ~/fedora-desktop
    ./setup.sh
    ```

## What Does This Script Do?

Refer to the scripts located in the `scripts` directory of this package for an extensive list of actions.

#### Packages

- Enables [RPM Fusion](https://rpmfusion.org) repos
- Installs any available updates
- Optionally installs [Nvidia GPU drivers](https://rpmfusion.org/Howto/NVIDIA)
- If [tinyMediaManager](https://www.tinymediamanager.org) is found installed at `~/.var/app/tinyMediaManager`, creates a .desktop for it
- Installs packages:
    - [dconf Editor](https://packages.fedoraproject.org/pkgs/dconf-editor/dconf-editor)
    - [Gnome Archive Manager](https://packages.fedoraproject.org/pkgs/file-roller/file-roller)
    - [Gnome Tweaks](https://packages.fedoraproject.org/pkgs/gnome-tweaks/gnome-tweaks)
    - [GOverlay](https://packages.fedoraproject.org/pkgs/goverlay/goverlay)
    - [libmediainfo](https://packages.fedoraproject.org/pkgs/libmediainfo/libmediainfo)
    - [MangoHud](https://packages.fedoraproject.org/pkgs/mangohud/mangohud)
    - [Steam](https://packages.fedoraproject.org/pkgs/steam/steam)
    - [steam-devices](https://packages.fedoraproject.org/pkgs/steam-devices/steam-devices)
    - [unrar](https://packages.fedoraproject.org/pkgs/unrar/unrar)
    - [wireguard-tools](https://packages.fedoraproject.org/pkgs/wireguard-tools/wireguard-tools)
- Uninstalls 'bloat' packages:
    - [Firefox](https://packages.fedoraproject.org/pkgs/firefox/firefox/), LibreWolf and UnGoogled Chromium Flatpaks are installed instead
    - [Gnome Boxes](https://packages.fedoraproject.org/pkgs/gnome-boxes/gnome-boxes), Flatpak version is installed instead
    - [Gnome Calendar](https://packages.fedoraproject.org/pkgs/gnome-calendar/gnome-calendar)
    - [Gnome Characters](https://packages.fedoraproject.org/pkgs/gnome-characters/gnome-characters)
    - [Gnome Clocks](https://packages.fedoraproject.org/pkgs/gnome-clocks/gnome-clocks)
    - [Gnome Contacts](https://packages.fedoraproject.org/pkgs/gnome-contacts/gnome-contacts)
    - [Gnome Logs](https://packages.fedoraproject.org/pkgs/gnome-logs/gnome-logs)
    - [Gnome Maps](https://packages.fedoraproject.org/pkgs/gnome-maps/gnome-maps)
    - [Gnome Music](https://packages.fedoraproject.org/pkgs/gnome-music/gnome-music)
    - [Gnome Photos](https://packages.fedoraproject.org/pkgs/gnome-photos/gnome-photos)
    - [Gnome Tour](https://packages.fedoraproject.org/pkgs/gnome-tour/gnome-tour)
    - [Gnome Weather](https://packages.fedoraproject.org/pkgs/gnome-weather/gnome-weather)
    - [Gnome Videos](https://packages.fedoraproject.org/pkgs/totem/totem)
    - [LibreOffice](https://packages.fedoraproject.org/pkgs/libreoffice/libreoffice), OnlyOffice Flatpak is installed instead
    - [Rhythmbox](https://packages.fedoraproject.org/pkgs/rhythmbox/rhythmbox)

#### Flatpaks

- Removes Fedora's default Flatpak repos, these are very limited and often slow to update
- Adds [Flathub](https://flathub.org) Flatpak repo
- Installs applications:
    - [FileZilla](https://flathub.org/apps/org.filezillaproject.Filezilla)
    - [FreeCAD](https://flathub.org/apps/org.freecadweb.FreeCAD)
    - [FreeTube](https://flathub.org/apps/io.freetubeapp.FreeTube)
    - [Gnome Boxes](https://flathub.org/apps/org.gnome.Boxes)
    - [Gnome Extension Manager](https://flathub.org/apps/com.mattjakeman.ExtensionManager)
    - [GNU Image Manipulation Program](https://flathub.org/apps/org.gimp.GIMP)
    - [Inkscape](https://flathub.org/apps/org.inkscape.Inkscape)
    - [Jitsi Meet](https://flathub.org/apps/org.jitsi.jitsi-meet)
    - [LibreWolf](https://flathub.org/apps/io.gitlab.librewolf-community)
    - [OBS Studio](https://flathub.org/apps/com.obsproject.Studio)
    - [OnlyOffice Desktop Editors](https://flathub.org/apps/org.onlyoffice.desktopeditors)
    - [ProtonUp-Qt](https://flathub.org/apps/net.davidotek.pupgui2)
    - [PrusaSlicer](https://flathub.org/apps/com.prusa3d.PrusaSlicer)
    - [qBittorrent](https://flathub.org/apps/org.qbittorrent.qBittorrent)
    - [Samplebrain](https://flathub.org/apps/org.thentrythis.Samplebrain)
    - [Signal Desktop](https://flathub.org/apps/org.signal.Signal)
    - [Spotify](https://flathub.org/apps/com.spotify.Client)
    - [SGDBoop](https://flathub.org/apps/com.steamgriddb.SGDBoop)
    - [Steam ROM Manager](https://flathub.org/apps/com.steamgriddb.steam-rom-manager)
    - [Tube Converter](https://flathub.org/apps/org.nickvision.tubeconverter)
    - [UnGoogled Chromium](https://flathub.org/apps/com.github.Eloston.UngoogledChromium)
    - [VLC Media Player](https://flathub.org/apps/org.videolan.VLC)
    - [VSCodium](https://flathub.org/apps/com.vscodium.codium)
    - [WatchMate](https://flathub.org/apps/io.gitlab.azymohliad.WatchMate)
- Optionally installs emulators:
    - [Dolphin](https://flathub.org/apps/org.DolphinEmu.dolphin-emu)
    - [DuckStation](https://flathub.org/apps/org.duckstation.DuckStation)
    - [mGBA](https://flathub.org/apps/io.mgba.mGBA)
    - [PCSX2](https://flathub.org/apps/net.pcsx2.PCSX2)
    - [Xemu](https://flathub.org/apps/org.ppsspp.PPSSPP)
- Optionally installs games:
    - [OpenRCT2](https://flathub.org/apps/io.openrct2.OpenRCT2)
    - [PolyMC Minecraft Launcher](https://flathub.org/apps/org.polymc.PolyMC)
    - [Sonic 3: Angel Island Revisited](https://flathub.org/apps/org.sonic3air.Sonic3AIR)
    - [Sonic Robo Blast 2 Kart](https://flathub.org/apps/org.srb2.SRB2Kart)
    - [Space Cadet Pinball](https://flathub.org/apps/com.github.k4zmu2a.spacecadetpinball)

#### JetBrains Toolbox

- Optionally installs [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app), used to manage JetBrains products such as Android Studio, Rider, and PyCharm

#### Gnome Shell Extensions

- Installs Gnome Shell extensions:
    - [AppIndicator and KStatusNotifierItem Support](https://extensions.gnome.org/extension/615/appindicator-support)
    - [Blur my Shell](https://extensions.gnome.org/extension/3193/blur-my-shell)
    - [Caffeine](https://extensions.gnome.org/extension/517/caffeine)
    - [Desktop Icons NG (DING)](https://extensions.gnome.org/extension/2087/desktop-icons-ng-ding)
    - [Quick Settings Audio Panel](https://extensions.gnome.org/extension/5940/quick-settings-audio-panel)

#### System Configuration

- Applies a set of dconf rules to configure system, extension, and application settings
- Applies a different background
- Applies a pre-configured app picker and favorites bar layout
- Sets default web browser to [LibreWolf](https://librewolf.net)
- Deletes some unused folders
- Installs udev rules for the [GameCube Controller Adapter for Wii U](https://wiki.dolphin-emu.org/index.php?title=How_to_use_the_Official_GameCube_Controller_Adapter_for_Wii_U_in_Dolphin#Linux)
- Enables MangoHud globally for all Vulkan applications
- Applies a default configuration for MangoHud

#### VPN Configuration

- Optionally configures and enables a WireGuard connection to [Mullvad VPN](https://mullvad.net)

## MangoHud

MangoHud is a performance monitoring overlay similar to MSI Afterburner or EVGA Precision X.

You can modify the layout, settings, key bindings, etc. for MangoHud using GOverlay.

#### Key Bindings

This script applies a basic default config file for MangoHud which uses the following key bindings:

- `Right Shift + F10` - Upload Log
- `Right Shift + F11` - Start / Stop Logging
- `Right Shift + F12` - Show / Hide MangoHud
