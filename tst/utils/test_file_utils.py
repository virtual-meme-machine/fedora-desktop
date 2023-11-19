import os
import shutil
import subprocess
import tempfile

from unittest.mock import patch

import pytest

from utils import file_utils


class MockCompletedProcess(object):
    """
    Mocked subprocess.CompletedProcess object
    """
    returncode: int
    stdout: str

    def __init__(self, returncode: int = 0, stdout: str = ""):
        self.returncode = returncode
        self.stdout = stdout


def mock_run_command_as_sudo(args: list[str]):
    """
    Mocked sudo_utils.run_command_as_sudo()
    :param args: List of command arguments
    :return: None
    """
    subprocess.run(args)


def mock_subprocess_curl(args: list[str] = [],
                         capture_output: bool = False,
                         check: bool = False,
                         stdout: None = None,
                         text: bool = False) -> MockCompletedProcess:
    """
    Mocked subprocess.run() that returns an empty MockCompletedProcess
    :param args: List of command arguments
    :param capture_output: Boolean that denotes if command output should be captured
    :param check: Boolean that denotes if an exception should be thrown if command fails
    :param stdout: IO interface where stdout should be sent
    :param text: Boolean that denotes if output should be decoded to string
    :return: MockCompletedProcess object
    """
    return MockCompletedProcess()


def test_importable():
    """
    Tests that the module can be imported
    :return: None
    """
    import utils.file_utils  # noqa: F401


class TestFileUtils:
    """
    Tests utils.file_utils functions
    Generates a temp dir on initialization and deletes it on de-initialization
    """
    temp_dir = tempfile.mkdtemp()

    def __del__(self):
        """
        Cleans up generated files when class is de-initialized
        :return: None
        """
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_delete_path(self):
        """
        Tests delete_path() with the following use cases:
        - Path does not exist
        - Path is a file
        - Path is a symlink
        - Path is a directory
        :return: None
        """
        does_not_exist = os.path.join(self.temp_dir, "does_not_exist")
        test_file = os.path.join(self.temp_dir, "test_file.txt")
        test_symlink = os.path.join(self.temp_dir, "test_symlink")
        test_dir = os.path.join(self.temp_dir, "test_dir")

        # Test deleting a path that does not exist
        assert not os.path.exists(does_not_exist)
        file_utils.delete_path(does_not_exist)
        assert not os.path.exists(does_not_exist)

        # Test deleting file
        with open(test_file, "w") as file:
            file.write("testing123")
        assert os.path.isfile(test_file)
        file_utils.delete_path(test_file)
        assert not os.path.isfile(test_file)

        # Test deleting symlink
        os.symlink(self.temp_dir, test_symlink)
        assert os.path.islink(test_symlink)
        file_utils.delete_path(test_symlink)
        assert not os.path.islink(test_symlink)

        # Test deleting directory
        os.mkdir(test_dir)
        assert os.path.isdir(test_dir)
        file_utils.delete_path(test_dir)
        assert not os.path.isdir(test_dir)

    def test_download_file(self):
        """
        Tests download_file() with the following use cases:
        - URL and path are valid, download is successful
        - URL is invalid, download raises exception
        :return: None
        """
        file_url = "https://github.githubassets.com/favicons/favicon.png"
        file_path = os.path.join(self.temp_dir, "favicon.png")

        file_utils.download_file(file_url, file_path)
        assert os.path.isfile(file_path)

        with pytest.raises(subprocess.CalledProcessError):
            file_utils.download_file("not_valid", file_path)

    @patch("utils.file_utils.subprocess.run", new=mock_subprocess_curl)
    def test_download_file_no_file(self):
        """
        Tests download_file() with the following use cases:
        - Download is process returns successful but file does not exist
        :return: None
        """
        file_path = os.path.join(self.temp_dir, "not_a_file.txt")

        with pytest.raises(FileNotFoundError):
            file_utils.download_file("not_a_url", file_path)

    @patch("utils.file_utils.run_command_as_sudo", new=mock_run_command_as_sudo)
    def test_write_system_file(self):
        """
        Tests write_system_file() with the following use cases:
        - File is written successfully
        :return: None
        """
        file_path = os.path.join(self.temp_dir, "test_system_file.txt")
        file_utils.write_system_file(file_path, ["testing", "123"])

        assert os.path.isfile(file_path)
