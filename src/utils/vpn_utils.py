import os
import subprocess
import tempfile


def generate_wireguard_private_key() -> str:
    """
    Generates a new WireGuard private key and returns it
    :return: New WireGuard private key as a string
    """
    return subprocess.check_output(["/usr/bin/wg", "genkey"], text=True).strip()


def generate_wireguard_public_key(private_key: str) -> str:
    """
    Generates a new WireGuard public key and returns it
    :param private_key: Private key that we want to generate an associated public key for
    :return: New WireGuard public key as a string
    """
    return subprocess.check_output(["/usr/bin/wg", "pubkey"], input=private_key, text=True).strip()


def import_wireguard_config(connection_name: str, config_data: list[str]):
    """
    Imports a WireGuard VPN config into NetworkManager
    :param connection_name: Name of the WireGuard connection
    :param config_data: Contents of the WireGuard config
    :return: None
    """
    config_file = os.path.join(tempfile.mkdtemp(), f"{connection_name}.conf")

    print(f"Writing WireGuard config to temporary file: '{config_file}'")
    with open(config_file, "w") as config:
        for line in config_data:
            config.write(line)
            config.write("\n")

    print(f"Importing WireGuard config '{connection_name}'")
    subprocess.check_call(["/usr/bin/nmcli", "connection", "import", "type", "wireguard", "file", config_file])
    os.remove(config_file)


def is_wireguard_connection_active():
    """
    Checks if a WireGuard connection is currently active
    :return: True if WireGuard connection is active, False if not
    """
    return "wireguard" in subprocess.check_output(["/usr/bin/nmcli", "connection", "show", "--active"], text=True)
