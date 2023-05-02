import os

from utils.file_utils import write_system_file

GC_ADAPTER_UDEV_FILE: str = "/etc/udev/rules.d/51-gcadapter.rules"
GC_ADAPTER_UDEV_RULES: str = "UBSYSTEM==\"usb\", " \
                             "ENV{DEVTYPE}==\"usb_device\", " \
                             "ATTRS{idVendor}==\"057e\", " \
                             "ATTRS{idProduct}==\"0337\", " \
                             "MODE=\"0666\""


def execute():
    """
    Installs udev rules for the GameCube Controller Adapter for Wii U
    :return: None
    """
    if os.path.isfile(GC_ADAPTER_UDEV_FILE):
        print("Udev rules for the GameCube Controller Adapter for Wii U already exist")
        return

    print(f"Writing udev rules to file: '{GC_ADAPTER_UDEV_FILE}'")
    write_system_file(GC_ADAPTER_UDEV_FILE, [GC_ADAPTER_UDEV_RULES])
