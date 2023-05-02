import os
import shutil
import subprocess
import tempfile


def delete_path(path: str):
    """
    Attempts to delete the object at the given path
    :param path: Path to the object we want to delete, eg: "/home/user/Downloads/file.txt"
    :return: None
    """
    if not os.path.exists(path):
        return

    if os.path.isfile(path):
        print(f"Deleting file: '{path}'")
        os.remove(path)

    elif os.path.islink(path):
        print(f"Deleting symlink: '{path}'")
        os.unlink(path)

    elif os.path.isdir(path):
        print(f"Deleting folder: '{path}'")
        shutil.rmtree(path)


def download_file(url: str, output: str):
    """
    Downloads a file to a local path on the system
    :param url: URL of the file we want to download, eg: "https://example.com/file.txt"
    :param output: Local path the file should be saved to, eg: "/home/user/Downloads/file.txt"
    :return: None
    """
    print(f"Downloading '{url}' to '{output}'")
    subprocess.check_call(["/usr/bin/curl", "-Ls", url, "--output", output])

    if not os.path.isfile(output):
        raise FileNotFoundError(f"Failed to download file '{url}'")


def write_system_file(file_path: str, lines: list[str]):
    """
    Writes to a system file by writing to a temp file and then copying the temp file to the desired path
    :param file_path: Path to the system file we want to write to
    :param lines: List of lines that should be written to the file
    :return: None
    """
    temp_file = tempfile.mktemp()
    with open(temp_file, "w") as temp:
        temp.writelines(lines)
        temp.write("\n")

    subprocess.check_call(["/usr/bin/pkexec", "/usr/bin/cp", temp_file, file_path])
