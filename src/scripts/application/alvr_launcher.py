import os
import shutil
import tempfile

from utils.file_utils import download_file

DESKTOP_FILE: str = os.path.expanduser("~/.local/share/applications/ALVR-Launcher.desktop")
DOWNLOAD_URL: str = "https://github.com/alvr-org/ALVR/releases/download/v20.9.1/alvr_launcher_linux.tar.gz"
INSTALL_DIR: str = os.path.expanduser("~/.local/share/ALVR-Launcher")
ALVR_LAUNCHER_EXEC: str = os.path.join(INSTALL_DIR, "ALVR Launcher")


def __install():
    """
    Downloads ALVR Launcher and installs it
    :return: None
    """
    if os.path.isfile(ALVR_LAUNCHER_EXEC):
        print("ALVR Launcher is already installed")
        return

    temp_dir = tempfile.mkdtemp()
    download_path = os.path.join(temp_dir, os.path.basename(DOWNLOAD_URL))
    download_file(url=DOWNLOAD_URL, output=download_path)

    print("Installing...")
    shutil.unpack_archive(download_path, temp_dir)
    os.makedirs(INSTALL_DIR)
    shutil.move(os.path.join(temp_dir, "ALVR Launcher"), INSTALL_DIR)


def execute():
    """
    Installs ALVR Launcher
    :return: None
    """
    __install()

    if not os.path.isfile(DESKTOP_FILE):
        print(f"Creating .desktop file at '{DESKTOP_FILE}'")
        with open(DESKTOP_FILE, "w") as desktop_file:
            desktop_file.writelines([
                "[Desktop Entry]\n",
                "Type=Application\n",
                "Terminal=false\n",
                "Name=ALVR Launcher\n",
                "Categories=Game;\n",
                f"Exec=\"{ALVR_LAUNCHER_EXEC}\"\n"
            ])
