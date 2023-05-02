# Fedora Desktop Configurator

Automated post-installation configuration tool for Fedora Linux (Workstation Edition).

Supports Fedora Linux 37 as of April 2023. Fedora Linux 38 is mostly supported, your milage may vary.

## Usage

**!! DO NOT enable third-party repos if asked, this script will set up RPM Fusion and Flathub on its own !!**

1. Clean install [Fedora Linux](https://getfedora.org/en/workstation) on your host
2. Preform initial setup (creating an account, etc.)
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

## MangoHud

MangoHud is a performance monitoring overlay similar to MSI Afterburner or EVGA Precision X.

You can modify the layout, settings, key bindings, etc. for MangoHud using GOverlay.

#### Key Bindings

The 'Configure MangoHud' option applies a config file which uses the following key bindings:

- `Right Shift + F10` - Upload Log
- `Right Shift + F11` - Start / Stop Logging
- `Right Shift + F12` - Show / Hide MangoHud
