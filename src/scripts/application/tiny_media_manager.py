import os
import shutil
import tempfile

from utils.dnf_utils import install_packages
from utils.file_utils import download_file
from utils.platform_utils import symlink_to_local_bin

DESKTOP_FILE: str = os.path.expanduser("~/.local/share/applications/tinyMediaManager.desktop")
DOWNLOAD_URL: str = "https://archive.tinymediamanager.org/v5.0.13/tinyMediaManager-5.0.13-linux-amd64.tar.xz"
INSTALL_DIR: str = os.path.expanduser("~/.local/share/tinyMediaManager")
TMM_EXEC: str = os.path.join(INSTALL_DIR, "tinyMediaManager")
TMM_ICON: str = os.path.join(INSTALL_DIR, "tmm.png")


def __install():
    """
    Downloads tinyMediaManager and installs it
    :return: None
    """
    if os.path.isfile(TMM_EXEC):
        print("tinyMediaManager is already installed")
        return

    temp_dir = tempfile.mkdtemp()
    download_path = os.path.join(temp_dir, os.path.basename(DOWNLOAD_URL))
    download_file(url=DOWNLOAD_URL, output=download_path)

    print("Installing...")
    shutil.unpack_archive(download_path, temp_dir)
    shutil.move(os.path.join(temp_dir, "tinyMediaManager"), INSTALL_DIR)


def execute():
    """
    Installs tinyMediaManager
    :return: None
    """
    install_packages(["libmediainfo"])
    __install()
    symlink_to_local_bin(TMM_EXEC)

    if not os.path.isfile(DESKTOP_FILE):
        with open(DESKTOP_FILE, "w") as desktop_file:
            desktop_file.writelines([
                "[Desktop Entry]\n",
                "Type=Application\n",
                "Terminal=false\n",
                "Name=tinyMediaManager\n",
                "Categories=Utility;AudioVideo;\n",
                f"Icon={TMM_ICON}\n",
                f"Exec={TMM_EXEC}\n"
            ])
