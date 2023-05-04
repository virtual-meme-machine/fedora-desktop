import json
import os.path
import random
import re
import subprocess

from utils.dnf_utils import install_packages
from utils.file_utils import write_system_file

DNS_SERVER: str = "193.138.218.74"
PREFERRED_COUNTRY: str = "USA"
PROMPT_TEXT: str = "Please input your Mullvad VPN account ID"
PROMPT_TITLE: str = "Mullvad VPN Setup"
WIREGUARD_CONFIG_DIR: str = "/etc/wireguard"


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
    install_packages(["wireguard-tools"])

    if "wg-quick@" in subprocess.check_output(["/usr/bin/systemctl", "list-units", "--type=service", "--state=active"],
                                              text=True):
        print("WireGuard VPN connection is already configured")
        return

    account_id = __get_account_id()
    if account_id is False:
        return

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
    city_relays: list = random_city.get("relays")
    random_relay: dict = city_relays[random.randint(0, len(city_relays) - 1)]
    hostname: str = random_relay.get("hostname")

    if not os.path.isdir(WIREGUARD_CONFIG_DIR):
        subprocess.check_call(["/usr/bin/pkexec", "/usr/bin/mkdir", "-p", WIREGUARD_CONFIG_DIR])
    if not os.path.isdir(WIREGUARD_CONFIG_DIR):
        raise NotADirectoryError(f"Unable to create Wireguard config folder '{WIREGUARD_CONFIG_DIR}'")

    print("Writing config file")
    write_system_file(file_path=os.path.join(WIREGUARD_CONFIG_DIR, f"{hostname}.conf"),
                      lines=[
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

    print("Enabling WireGuard service")
    subprocess.check_call(["/usr/bin/pkexec", "/usr/bin/systemctl", "--now", "enable", f"wg-quick@{hostname}"])
