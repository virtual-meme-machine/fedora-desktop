# fedora-desktop

This package contains a set of scripts designed to configure a clean installation of Fedora Workstation.

Developed for and verified working on Fedora Workstation 37 (GNOME) as of January 2023.

## Usage

**!! DO NOT enable third-party repos if asked, this script will set up RPM Fusion and Flathub on its own !!**

1. Clean install [Fedora Workstation](https://getfedora.org/en/workstation/) on your host
2. Preform initial setup (creating an account, etc.)
3. Once at the desktop copy this package somewhere on the host (eg: `~/Downloads`)
4. Open a terminal and run `setup.sh`:
    ```bash
    cd ~/Downloads/fedora-desktop
    ./setup.sh
    ```

## What Does This Script Do?

Refer to the scripts located in the `scripts` directory of this package for an extensive list of actions.

#### Packages

- Uninstalls 'bloat' packages that come with Fedora Workstation, this is mostly useless apps like Gnome Weather
- Enables [RPM Fusion](https://rpmfusion.org/) package repos
- Installs any available updates
- Installs Nvidia GPU drivers
- Installs MangoHud and GOverlay, see MangoHud section below for more details
- Installs Steam
- Installs useful libraries such as `unrar` and `wireguard-tools`
- If TinyMediaManager is found installed at `~/.var/app/tinyMediaManager`, creates a .desktop for it

#### Flatpaks

- Removes Fedora's default Flatpak repos, these are very limited and often slow to update
- Adds Flathub Flatpak repo
- Installs Flatpaks for a variety of applications, emulators, and games

#### Gnome Shell Extensions

- Installs a set of Gnome Shell extensions that enhance the default Gnome experience

#### System Configuration

- Applies a set of dconf rules to configure system, extension, and application settings
- Applies a different background
- Applies a pre-configured app picker and favorites bar layout
- Sets default web browser to LibreWolf
- Deletes some unused folders
- Installs udev rules for the [GameCube Controller Adapter for Wii U](https://wiki.dolphin-emu.org/index.php?title=How_to_use_the_Official_GameCube_Controller_Adapter_for_Wii_U_in_Dolphin#Linux)
- Enables MangoHud globally for all Vulkan applications
- Applies a default configuration for MangoHud

#### VPN Configuration

- Optionally configures and enables a WireGuard connection to Mullvad VPN

## MangoHud

[MangoHud](https://github.com/flightlessmango/MangoHud) is a performance monitoring overlay similar to MSI Afterburner or EVGA Precision X.

You can modify the layout, settings, key bindings, etc. for MangoHud using GOverlay.

#### Key Bindings

This script applies a basic default config file for MangoHud which uses the following key bindings:

- `Right Shift + F10` - Upload Log
- `Right Shift + F11` - Start / Stop Logging
- `Right Shift + F12` - Show / Hide MangoHud
