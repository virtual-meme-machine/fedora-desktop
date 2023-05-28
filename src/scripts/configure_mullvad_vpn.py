import json
import os.path
import random
import re
import subprocess
import tempfile

from utils.dnf_utils import install_packages

DNS_SERVER: str = "193.138.218.74"
PREFERRED_COUNTRY: str = "USA"
PROMPT_TEXT: str = "Please input your Mullvad VPN account ID"
PROMPT_TITLE: str = "Mullvad VPN Setup"


def __get_account_id() -> str or False:
    """
    Prompts the user to provide their Mullvad VPN account ID via a GUI pop up
    :return: Account ID as a string, or False if user cancelled input
    """
    while True:
        print("Prompting for Mullvad VPN account ID")
        try:
            account_id = subprocess.check_output(["/usr/bin/zenity", "--entry", "--hide-text",
                                                  f"--title={PROMPT_TITLE}",
                                                  f"--text={PROMPT_TEXT}",
                                                  f"--ok-label=Submit"], text=True).strip()
        except subprocess.CalledProcessError as err:
            if err.returncode == 1:
                print("VPN configuration cancelled")
                return False

        if re.match(r"\d{16}", account_id):
            return account_id

        print("Account ID does not appear to be valid, please try again")


def execute():
    """
    Configures and enables a WireGuard connection to Mullvad VPN
    Based on: https://mullvad.net/media/files/mullvad-wg.sh
    :return: None
    """
    if "wireguard" in subprocess.check_output(["/usr/bin/nmcli", "connection", "show", "--active"],
                                              text=True):
        print("WireGuard VPN connection is already configured")
        return

    account_id = __get_account_id()
    if account_id is False:
        return

    install_packages(["wireguard-tools"])

    private_key = subprocess.check_output(["/usr/bin/wg", "genkey"], text=True).strip()
    public_key = subprocess.check_output(["/usr/bin/wg", "pubkey"], input=private_key, text=True).strip()

    print("Submitting keys to Mullvad API")
    server_address = subprocess.check_output(["/usr/bin/curl", "-LsS", "https://api.mullvad.net/wg/",
                                              "-d", f"account={account_id}",
                                              "--data-urlencode", f"pubkey={public_key}"], text=True).strip()
    if "Account does not exist" in server_address:
        raise ConnectionError("Unable to retrieve server address from Mullvad API")

    endpoint_data: dict = json.loads(subprocess.check_output(["/usr/bin/curl", "-LsS",
                                                              "https://api.mullvad.net/public/relays/wireguard/v1/"],
                                                             text=True).strip())
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

    print("Writing config file")
    config_file = os.path.join(tempfile.mkdtemp(), f"mullvad_{city_code}_wg0.conf")
    with open(config_file, "w") as config:
        config.writelines([
            f"[Interface]\n",
            f"PrivateKey = {private_key}\n",
            f"Address = {server_address}\n",
            f"DNS = {DNS_SERVER}\n",
            f"\n",
            f"[Peer]\n",
            f"PublicKey = {random_relay.get('public_key')}\n",
            f"Endpoint = {random_relay.get('ipv4_addr_in')}:51820\n",
            f"AllowedIPs = 0.0.0.0/0, ::/0"
        ])
        config.write("\n")

    print("Enabling WireGuard connection")
    subprocess.check_call(["/usr/bin/nmcli", "connection", "import", "type", "wireguard", "file", config_file])
    os.remove(config_file)
