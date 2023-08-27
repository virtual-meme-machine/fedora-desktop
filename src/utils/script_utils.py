import importlib.util
import os
import sys
from types import ModuleType

from data.Paths import SCRIPTS_DIR


def load_script(script_name: str) -> ModuleType:
    """
    Attempts to load a script in the scripts directory and return it
    :param script_name: Name of the script file without the file extension, eg: "remove_firefox"
    :return: Loaded module
    """
    module_name = f"script.{script_name}"
    script_path = os.path.join(SCRIPTS_DIR, f"{script_name}.py")

    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Unable to locate script '{script_name}', please ensure it exists at '{script_path}'")

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "execute"):
        raise FileNotFoundError(f"Unable to execute script '{script_name}', script does not have an execute method")

    return module
