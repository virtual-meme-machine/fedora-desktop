import os

PACKAGE_ROOT: str = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
DOCS_DIR: str = os.path.join(PACKAGE_ROOT, "docs")
RESOURCES_DIR: str = os.path.join(PACKAGE_ROOT, "resources")
SCRIPTS_DIR: str = os.path.join(PACKAGE_ROOT, "src", "scripts")

OPTIONS_DIR: str = os.path.join(RESOURCES_DIR, "options")
PROFILES_DIR: str = os.path.join(RESOURCES_DIR, "profiles")
