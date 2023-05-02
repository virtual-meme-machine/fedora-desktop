import os

from utils.file_utils import write_system_file

CONFIG: str = """
# Overlay layout
legacy_layout=false
gpu_stats
gpu_temp
gpu_load_change
gpu_load_value=50,90
gpu_load_color=FFFFFF,FFAA7F,CC0000
gpu_text=GPU
cpu_stats
cpu_temp
cpu_load_change
core_load_change
cpu_load_value=50,90
cpu_load_color=FFFFFF,FFAA7F,CC0000
cpu_color=2e97cb
cpu_text=CPU
io_color=a491d3
vram
vram_color=ad64c1
ram
ram_color=c26693
fps
engine_color=eb5b5b
gpu_color=2e9762
wine_color=eb5b5b
frame_timing=1
frametime_color=00ff00
media_player_color=ffffff
background_alpha=0.2
font_size=24

# Overlay position and style
background_color=020202
position=top-left
text_color=ffffff
round_corners=5

# Key Bindings
upload_log=Shift_R+F10
toggle_logging=Shift_R+F11
toggle_hud=Shift_R+F12
"""
CONFIG_DIR: str = os.path.expanduser("~/.config/MangoHud")
CONFIG_FILE: str = os.path.join(CONFIG_DIR, "MangoHud.conf")
SYSTEM_ENVIRONMENT_FILE: str = "/etc/environment"


def __create_config():
    """
    Generates a MangoHud config file
    :return: None
    """
    if os.path.isfile(CONFIG_FILE):
        print(f"MangoHud config file already exists")
        return

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    print("Generating MangoHud config file")
    with open(CONFIG_FILE, "w") as config_file:
        config_file.write(CONFIG)
        config_file.write("\n")


def __enable_globally():
    """
    Enables MangoHud globally for all Vulkan applications
    :return: None
    """
    env_lines: list[str] = []

    with open(SYSTEM_ENVIRONMENT_FILE, "r") as env_file:
        env_lines.extend(env_file.read().strip().split("\n"))

    if "MANGOHUD=1" in env_lines:
        print("MangoHud already enabled globally")
        return

    print("Enabling MangoHud globally for all Vulkan applications")
    env_lines.append("MANGOHUD=1")
    write_system_file(SYSTEM_ENVIRONMENT_FILE, env_lines)


def execute():
    """
    Configures MangoHud and enables it for all Vulkan applications
    :return: None
    """
    __create_config()
    __enable_globally()
