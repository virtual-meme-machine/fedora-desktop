from utils.dnf_utils import install_packages
from utils.file_utils import write_system_file
from utils.flatpak_utils import install_flatpaks

I2C_DEV_CONF_FILE: str = "/etc/modules-load.d/i2c-dev.conf"
I2C_DEV_CONTENTS: str = "i2c-dev"


def execute():
    """
    Installs OpenRGB
    :return: None
    """
    install_packages(["openrgb-udev-rules"])
    install_flatpaks(["org.openrgb.OpenRGB"])

    print(f"Setting kernel module 'i2c-dev' to load on startup")
    write_system_file(I2C_DEV_CONF_FILE, [I2C_DEV_CONTENTS])
