# Fedora Desktop Configurator

Automated post-installation configuration tool for Fedora Linux (Workstation Edition).

Supports Fedora Linux 37 as of April 2023. Fedora Linux 38 is mostly supported, your milage may vary.

![preview](docs/images/preview.png)

## Usage

**!! DO NOT enable third-party repos if asked, this script will set up RPM Fusion and Flathub on its own !!**

1. Clean install [Fedora Linux](https://www.fedoraproject.org/en/workstation/download) on your host
    1. [Fedora Linux 37 Live ISO](https://download.fedoraproject.org/pub/fedora/linux/releases/37/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-37-1.7.iso)
    2. [Fedora Linux 38 Live ISO](https://download.fedoraproject.org/pub/fedora/linux/releases/38/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-38-1.6.iso)
2. Preform initial setup (create an account, etc.)
3. Once at the desktop, open a terminal and git clone this package somewhere on the host:
    ```none
    git clone https://github.com/virtual-meme-machine/fedora-desktop.git ~/fedora-desktop
    ```
4. Enter the package directory and run `main.py`:
    ```none
    cd ~/fedora-desktop
    ./src/main.py
    ```
5. Select the configuration actions you want the tool to preform, then click 'Begin Setup'

## What Does This Do?

See [Options](docs/Options.md) for a complete list of actions this tool can preform.

## Steam

Steam for Linux can run most Windows games via a compatibility layer called Proton.

Proton is included with Steam but disabled by default,
[this tutorial](https://steamcommunity.com/sharedfiles/filedetails/?id=1974055703)
details how to enable Proton as well as some advanced options.

[ProtonDB](https://www.protondb.com) is a great resource for checking how well a game will run via Proton.

## MangoHud

MangoHud is a performance monitoring overlay similar to MSI Afterburner or EVGA Precision X.

You can modify the layout, settings, key bindings, etc. for MangoHud using GOverlay.

#### Key Bindings

The 'Configure MangoHud' option applies a config file which uses the following key bindings:

- `Right Shift + F10` - Upload Log
- `Right Shift + F11` - Start / Stop Logging
- `Right Shift + F12` - Show / Hide MangoHud
