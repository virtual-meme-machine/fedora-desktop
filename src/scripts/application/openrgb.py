import os

from utils.file_utils import write_system_file

I2C_DEV_CONF_FILE: str = "/etc/modules-load.d/i2c-dev.conf"
I2C_DEV_CONTENTS: str = "i2c-dev"


def execute():
    """
    Installs OpenRGB
    :return: None
    """
    if os.path.isfile(I2C_DEV_CONF_FILE):
        print("Kernel module 'i2c-dev' is already set to load on startup")
        return

    print(f"Setting kernel module 'i2c-dev' to load on startup")
    write_system_file(I2C_DEV_CONF_FILE, [I2C_DEV_CONTENTS])
