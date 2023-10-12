import json
import os
import shutil
import subprocess
import tempfile

from utils.file_utils import download_file
from utils.platform_utils import symlink_to_local_bin

RELEASE_INFO_URL: str = "https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release"
RELEASE_INFO_USER_AGENT: str = "User-Agent: Mozilla/5.0 (X11; Linux x86_64) " \
                               "AppleWebKit/537.36 (KHTML, like Gecko) " \
                               "Chrome/59.0.3071.115 Safari/537.36"
TOOLBOX_EXEC: str = os.path.expanduser("~/.local/share/JetBrains/Toolbox/bin/jetbrains-toolbox")


def __install():
    """
    Downloads JetBrains Toolbox and installs it
    :return: None
    """
    if os.path.isfile(TOOLBOX_EXEC):
        print("JetBrains Toolbox is already installed")
        return

    download_info = json.loads(subprocess.run(["/usr/bin/curl", "-s", RELEASE_INFO_URL,
                                               "-H", "Origin: https://www.jetbrains.com",
                                               "-H", "Accept-Encoding: gzip, deflate, br",
                                               "-H", "Accept-Language: en-US,en;q=0.8",
                                               "-H", RELEASE_INFO_USER_AGENT,
                                               "-H", "Accept: application/json, text/javascript, */*; q=0.01",
                                               "-H", "Referer: https://www.jetbrains.com/toolbox/download/",
                                               "-H", "Connection: keep-alive",
                                               "-H", "DNT: 1",
                                               "--compressed"], capture_output=True).stdout)

    if "TBA" not in download_info.keys():
        raise ValueError(f"Unable to determine JetBrains Toolbox download URL")

    temp_dir = tempfile.mkdtemp()
    download_url = download_info.get("TBA")[0].get("downloads").get("linux").get("link")
    download_path = os.path.join(temp_dir, os.path.basename(download_url))
    download_file(url=download_url, output=download_path)

    print("Installing...")
    shutil.unpack_archive(download_path, temp_dir)
    subprocess.run([os.path.join(temp_dir,
                                 os.path.basename(download_path).replace(".tar.gz", ""),
                                 "jetbrains-toolbox")], check=True)


def execute():
    """
    Installs JetBrains Toolbox
    Based on: https://github.com/nagygergo/jetbrains-toolbox-install
    :return: None
    """
    __install()
    symlink_to_local_bin(TOOLBOX_EXEC)
