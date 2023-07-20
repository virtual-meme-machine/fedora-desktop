import random
import re
import subprocess

from utils.dnf_utils import install_packages
from utils.vpn_utils import generate_wireguard_private_key, generate_wireguard_public_key, import_wireguard_config, \
    is_wireguard_connection_active

DNS_SERVER: str = "DNS=10.31.33.8"
IPV4_REGEX: str = r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
SERVER_DATA: dict[str, str] = {
    "la": "O3XwQl4+/ZIrqXJgKiXWWK+26+z+KHYL1GaCTX6/TSg=",
    "dc": "Vspvv1C5C/JAAcoysAdGzHUz98V0vYXLl8a5Yv3Xa3g=",
    "florida": "XYIg/q1hGyZ/8rRHgt2wKO4WtObzCyA4f8C8nMZWIA8=",
    "atlanta": "EZZUsR5l+Oe47s5900Q1JamvMYF6HB2Dbs6+ZAhXAzU=",
    "chicago": "ZQlqH2OjXnI7vhrc4HwSv9l1i8riD78p2hhmz+7bCj4=",
    "vegas": "wwQ63AoaSxBm1K9zCwl2XSmvwI8ADIx3Qponm1+AbWQ=",
    "maine": "lUN2Vqs+CswowhSS81X0cdkfMZe3hLnr0HznBegvilc=",
    "newyork": "IfiYOThU72ivKQncq1+jhQXYs6F2wBtZsUPHaeCccyA=",
    "nc": "s2ozcv7uGcvryYUs460wUE6xeouR+I2kqOjJvag91zI=",
    "oregon": "lUN2Vqs+CswowhSS81X0cdkfMZe3hLnr0HznBegvilc=",
    "dallas": "qrZ3+Jp0y2+eYlOE0heVBfFzcHhuWJ31Y5UF/mHQLRA=",
    "seattle": "3bHLNdTY/9AETg9OKgTsab+SjRitGqB+o4BH4gkzux8="
}


def __get_connection_info(public_key: str) -> (str, str) or None:
    """
    Prompts the user to provide their CryptoStorm connection info, this would be an IP address and a pre-shared key
    :param public_key: Generated public key that needs to be registered with CryptoStorm
    :return: Provided server IP address and pre-shared key
    """
    try:
        subprocess.check_call(["/usr/bin/zenity", "--info",
                               "--title=CryptoStorm Setup",
                               "--text=Please register your WireGuard public key at: https://cryptostorm.is/wireguard\n"
                               "You will input the provided IP address and pre-shared key in the next dialog."
                               "\n\n\n"
                               f"Your public key: <b>{public_key}</b>",
                               "--ok-label=Next"])
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            return None, None

    while True:
        try:
            account_info = subprocess.check_output(["/usr/bin/zenity", "--forms",
                                                    "--title=CryptoStorm Setup",
                                                    "--text=Connection Info",
                                                    "--add-entry=IP Address",
                                                    "--add-entry=Pre-Shared Key",
                                                    "--ok-label=Submit"], text=True).strip()
        except subprocess.CalledProcessError as err:
            if err.returncode == 1:
                return None, None

        input_list = account_info.split("|")
        if len(input_list) == 2:
            if re.match(IPV4_REGEX, input_list[0]) and re.match(r"\S{43}=", input_list[1]):
                return input_list[0], input_list[1]

        print("Connection info does not appear to be valid, please try again")


def execute():
    """
    Configures and enables a WireGuard connection to CryptoStorm
    Based on: https://cryptostorm.is/wg_confgen.txt
    :return: None
    """
    if is_wireguard_connection_active():
        print("A WireGuard VPN connection is already configured, skipping")
        return

    install_packages(["wireguard-tools"])
    private_key = generate_wireguard_private_key()
    public_key = generate_wireguard_public_key(private_key)
    server_ip, pre_shared_key = __get_connection_info(public_key)
    if server_ip is None or pre_shared_key is None:
        print("VPN configuration cancelled")
        return

    server_name = random.choice(list(SERVER_DATA.keys()))
    server_public_key = SERVER_DATA.get(server_name)

    import_wireguard_config(connection_name=f"cs_{server_name}_wg0",
                            config_data=[
                                f"[Interface]",
                                f"PrivateKey = {private_key}",
                                f"Address = {server_ip}",
                                f"DNS = {DNS_SERVER}",
                                f"",
                                f"[Peer]",
                                f"Presharedkey = {pre_shared_key}",
                                f"PublicKey = {server_public_key}",
                                f"Endpoint = {server_name}.cstorm.is:443",
                                f"AllowedIPs = 0.0.0.0/0",
                                f"PersistentKeepalive = 25"
                            ])
