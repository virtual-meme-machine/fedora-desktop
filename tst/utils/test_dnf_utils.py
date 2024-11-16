from unittest.mock import patch

from utils import dnf_utils


class MockCompletedProcess(object):
    """
    Mocked subprocess.CompletedProcess object
    """
    returncode: int
    stdout: str

    def __init__(self, returncode: int = 0, stdout: str = ""):
        self.returncode = returncode
        self.stdout = stdout


def mock__enable_rpmfusion_repos():
    """
    Mocked dnf_utils.__enable_rpmfusion_repos()
    :return: None
    """
    print("Enabling RPMFusion repos...")
    return


def mock_get_fedora_version() -> int:
    """
    Mocked platform_utils.get_fedora_version()
    :return: Predefined version number
    """
    return 37


def mock__get_package_list() -> list[str]:
    """
    Mocked dnf_utils.__get_package_list()
    :return: Predefined package list
    """
    return ["linux", "firefox"]


def mock__get_repo_list() -> list[str]:
    """
    Mocked dnf_utils.__get_repo_list()
    :return: Predefined repo list
    """
    return ["fedora", "updates"]


def mock_run_command_as_sudo(args: list[str]):
    """
    Mocked sudo_utils.run_command_as_sudo()
    :param args: List of command arguments
    :return: None
    """
    print(f"mock_run_command_as_sudo called: '{args}'")
    return


def mock_subprocess_run_invalid(args: list[str] = [],
                                capture_output: bool = False,
                                check: bool = False,
                                stdout: None = None,
                                text: bool = False) -> MockCompletedProcess:
    """
    Mocked subprocess.run() that returns 'invalid' values
    :param args: List of command arguments
    :param capture_output: Boolean that denotes if command output should be captured
    :param check: Boolean that denotes if an exception should be thrown if command fails
    :param stdout: IO interface where stdout should be sent
    :param text: Boolean that denotes if output should be decoded to string
    :return: MockCompletedProcess object
    """
    print(f"mock_subprocess_run_valid called: '{args}'")
    if args == [dnf_utils.DNF_EXEC, dnf_utils.DNF_NON_INTERACTIVE_FLAG, "list", "--autoremove"]:
        return MockCompletedProcess(stdout="null")  # No packages can be removed
    elif args == [dnf_utils.DNF_EXEC, dnf_utils.DNF_NON_INTERACTIVE_FLAG, "check-upgrade", "--refresh"]:
        return MockCompletedProcess(returncode=0)  # No updates can be installed


def mock_subprocess_run_valid(args: list[str] = [],
                              capture_output: bool = False,
                              check: bool = False,
                              stdout: None = None,
                              text: bool = False) -> MockCompletedProcess:
    """
    Mocked subprocess.run() that returns 'valid' values
    :param args: List of command arguments
    :param capture_output: Boolean that denotes if command output should be captured
    :param check: Boolean that denotes if an exception should be thrown if command fails
    :param stdout: IO interface where stdout should be sent
    :param text: Boolean that denotes if output should be decoded to string
    :return: MockCompletedProcess object
    """
    print(f"mock_subprocess_run_valid called: '{args}'")
    if args == [dnf_utils.DNF_EXEC, dnf_utils.DNF_NON_INTERACTIVE_FLAG, "list", "--autoremove"]:
        return MockCompletedProcess(stdout="Autoremove Packages")  # Packages can be removed
    elif args == [dnf_utils.DNF_EXEC, dnf_utils.DNF_NON_INTERACTIVE_FLAG, "check-upgrade", "--refresh"]:
        return MockCompletedProcess(returncode=1)  # Updates can be installed
    elif args == [dnf_utils.DNF_EXEC, dnf_utils.DNF_NON_INTERACTIVE_FLAG, "list", "--installed"]:
        return MockCompletedProcess(stdout="Installed Packages\n"
                                           "ModemManager.x86_64               "
                                           "1.18.12-1.fc37                    "
                                           "@updates                        \n"
                                           "NetworkManager.x86_64             "
                                           "1:1.40.18-1.fc37                  "
                                           "@updates                        \n")
    elif args == [dnf_utils.DNF_EXEC, dnf_utils.DNF_NON_INTERACTIVE_FLAG, "repolist"]:
        return MockCompletedProcess(stdout="repo id                        repo name\n"
                                           "fedora                         Fedora 37 - x86_64\n"
                                           "fedora-cisco-openh264          Fedora 37 openh264 (From Cisco) - x86_64\n"
                                           "fedora-modular                 Fedora Modular 37 - x86_64\n"
                                           "updates                        Fedora 37 - x86_64 - Updates\n"
                                           "updates-modular                Fedora Modular 37 - x86_64 - Updates\n")


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import utils.dnf_utils  # noqa: F401


@patch("utils.dnf_utils.__get_repo_list", new=mock__get_repo_list)
@patch("utils.dnf_utils.get_fedora_version", new=mock_get_fedora_version)
@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_valid)
def test__enable_rpmfusion_repos(capfd):
    """
    Tests __enable_rpmfusion_repos() with the following use cases:
    - Repos need to be enabled
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.__enable_rpmfusion_repos()
    out, err = capfd.readouterr()
    assert "mock_run_command_as_sudo called" in out
    assert f"rpmfusion-free-release-{mock_get_fedora_version()}.noarch.rpm" in out
    assert f"rpmfusion-nonfree-release-{mock_get_fedora_version()}.noarch.rpm" in out


@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_valid)
def test__get_package_list():
    """
    Tests __get_package_list() with the following use cases:
    - List of packages is returned by dnf
    :return: None
    """
    assert dnf_utils.__get_package_list() == ["ModemManager", "NetworkManager"]


@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_valid)
def test__get_repo_list():
    """
    Tests __get_repo_list() with the following use cases:
    - List of repos is returned by dnf
    :return: None
    """
    assert dnf_utils.__get_repo_list() == [
        "fedora",
        "fedora-cisco-openh264",
        "fedora-modular",
        "updates",
        "updates-modular"
    ]


@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_valid)
def test_auto_remove_packages(capfd):
    """
    Tests auto_remove_packages() with the following use cases:
    - Packages can be removed
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.auto_remove_packages()
    out, err = capfd.readouterr()
    assert "mock_subprocess_run_valid called" in out
    assert "mock_run_command_as_sudo called" in out


@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_invalid)
def test_auto_remove_packages_no_packages(capfd):
    """
    Tests auto_remove_packages() with the following use cases:
    - No packages can be removed
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.auto_remove_packages()
    out, err = capfd.readouterr()
    assert "mock_subprocess_run_valid called" in out
    assert "No unused dependencies to remove" in out


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
def test_install_packages(capfd):
    """
    Tests install_packages() with the following use cases:
    - Package list includes packages that need to be installed, installation is triggered
    :param capfd: pytest capture object
    :return: None
    """
    package_list = ["package"]

    dnf_utils.install_packages(package_list=package_list)
    out, err = capfd.readouterr()
    assert f"Installing RPM packages: {package_list}" in out
    assert "mock_run_command_as_sudo called" in out


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
def test_install_packages_no_packages(capfd):
    """
    Tests install_packages() with the following use cases:
    - Packages are already installed, nothing to do
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.install_packages(package_list=mock__get_package_list())
    out, err = capfd.readouterr()
    assert out == "Selected packages are already installed\n"


@patch("utils.dnf_utils.__enable_rpmfusion_repos", new=mock__enable_rpmfusion_repos)
@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
def test_install_packages_rpmfusion(capfd):
    """
    Tests install_packages() with the following use cases:
    - Package list includes packages that need to be installed, rpmfusion is enabled, installation is triggered
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.install_packages(package_list=["package"], rpmfusion=True)
    out, err = capfd.readouterr()
    assert "Enabling RPMFusion repos..." in out
    assert "mock_run_command_as_sudo called" in out


@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_valid)
def test_install_updates(capfd):
    """
    Tests install_updates() with the following use cases:
    - Updates are available
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.install_updates()
    out, err = capfd.readouterr()
    assert "mock_run_command_as_sudo called" in out


@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
@patch("utils.dnf_utils.subprocess.run", new=mock_subprocess_run_invalid)
def test_install_updates_no_updates(capfd):
    """
    Tests install_updates() with the following use cases:
    - No updates are available
    :param capfd: pytest capture object
    :return: None
    """
    dnf_utils.install_updates()
    out, err = capfd.readouterr()
    assert "No updates available" in out


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
def test_is_package_installed():
    """
    Tests is_package_installed() with the following use cases:
    - Package is installed
    - Package is not installed
    :return:
    """
    assert dnf_utils.is_package_installed(mock__get_package_list()[0]) is True
    assert dnf_utils.is_package_installed("package") is False


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
def test_remove_packages(capfd):
    """
    Tests remove_packages() with the following use cases:
    - Packages can be removed, remove is triggered
    :param capfd: pytest capture object
    :return: None
    """
    package_list = mock__get_package_list()

    dnf_utils.remove_packages(package_list)
    out, err = capfd.readouterr()
    assert f"Removing RPM packages: {package_list}" in out
    assert "mock_run_command_as_sudo called" in out


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
def test_remove_packages_no_packages(capfd):
    """
    Tests remove_packages() with the following use cases:
    - No packages can be removed, nothing to do
    :param capfd: pytest capture object
    :return: None
    """
    package_list = ["package"]

    dnf_utils.remove_packages(package_list)
    out, err = capfd.readouterr()
    assert out == "Selected packages have already been removed\n"


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
@patch("utils.dnf_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
def test_remove_packages_wildcard(capfd):
    """
    Tests remove_packages() with the following use cases:
    - Packages can be removed, remove is triggered
    :param capfd: pytest capture object
    :return: None
    """
    package_list = [f"{mock__get_package_list()[0]}*"]

    dnf_utils.remove_packages(package_list)
    out, err = capfd.readouterr()
    assert f"Removing RPM packages: {package_list}" in out
    assert "mock_run_command_as_sudo called" in out


@patch("utils.dnf_utils.__get_package_list", new=mock__get_package_list)
def test_remove_packages_wildcard_no_packages(capfd):
    """
    Tests remove_packages() with the following use cases:
    - Packages can be removed, remove is triggered
    :param capfd: pytest capture object
    :return: None
    """
    package_list = ["package*"]

    dnf_utils.remove_packages(package_list)
    out, err = capfd.readouterr()
    assert out == "Selected packages have already been removed\n"
