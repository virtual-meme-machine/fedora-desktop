import json
import random
import re
import subprocess

from utils.dnf_utils import install_packages
from utils.vpn_utils import generate_wireguard_private_key, generate_wireguard_public_key, import_wireguard_config, \
    is_wireguard_connection_active

DNS_SERVER: str = "193.138.218.74"
PREFERRED_COUNTRY: str = "USA"


def __get_account_id() -> str or None:
    """
    Prompts the user to provide their Mullvad VPN account ID via a GUI pop up
    :return: Account ID as a string, or False if user cancelled input
    """
    while True:
        print("Prompting for Mullvad VPN account ID")
        try:
            account_id = subprocess.run(["/usr/bin/zenity", "--entry", "--hide-text",
                                         "--title=Mullvad VPN Setup",
                                         "--text=Please input your Mullvad VPN account ID",
                                         "--ok-label=Submit"], capture_output=True, text=True).stdout.strip()
        except subprocess.CalledProcessError as err:
            if err.returncode == 1:
                print("VPN configuration cancelled")
                return None

        if re.match(r"\d{16}", account_id):
            return account_id

        print("Account ID does not appear to be valid, please try again")


def execute():
    """
    Configures and enables a WireGuard connection to Mullvad VPN
    Based on: https://mullvad.net/media/files/mullvad-wg.sh
    :return: None
    """
    if is_wireguard_connection_active():
        print("A WireGuard VPN connection is already configured, skipping")
        return

    account_id = __get_account_id()
    if account_id is None:
        return

    install_packages(["wireguard-tools"])
    private_key = generate_wireguard_private_key()
    public_key = generate_wireguard_public_key(private_key)

    print("Submitting keys to Mullvad API")
    server_address = subprocess.run(["/usr/bin/curl", "-LsS", "https://api.mullvad.net/wg/",
                                     "-d", f"account={account_id}",
                                     "--data-urlencode", f"pubkey={public_key}"],
                                    capture_output=True,
                                    text=True).stdout.strip()
    if "Account does not exist" in server_address:
        raise ConnectionError("Unable to retrieve server address from Mullvad API")

    endpoint_data: dict = json.loads(subprocess.run(["/usr/bin/curl", "-LsS",
                                                     "https://api.mullvad.net/public/relays/wireguard/v1/"],
                                                    capture_output=True,
                                                    text=True).stdout.strip())
    if "countries" not in endpoint_data.keys():
        raise ConnectionError("Unable to retrieve endpoint data from Mullvad API")

    country_data: dict = next((i for i in endpoint_data.get("countries") if i["name"] == PREFERRED_COUNTRY), None)
    if country_data is None:
        raise ConnectionError("Unable to retrieve endpoint data from Mullvad API")

    city_data: list = country_data.get("cities")
    random_city: dict = city_data[random.randint(0, len(city_data) - 1)]
    city_code: str = random_city.get("code")
    city_relays: list = random_city.get("relays")
    random_relay: dict = city_relays[random.randint(0, len(city_relays) - 1)]

    import_wireguard_config(connection_name=f"mv_{city_code}_wg0",
                            config_data=[
                                f"[Interface]",
                                f"PrivateKey = {private_key}",
                                f"Address = {server_address}",
                                f"DNS = {DNS_SERVER}",
                                f"",
                                f"[Peer]",
                                f"PublicKey = {random_relay.get('public_key')}",
                                f"Endpoint = {random_relay.get('ipv4_addr_in')}:51820",
                                f"AllowedIPs = 0.0.0.0/0, ::/0"
                            ])
