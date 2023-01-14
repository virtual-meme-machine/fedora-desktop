#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  configure_vpn.sh                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
#  Based on 'mullvad-wg.sh'                                                                                            #
#  Source: https://mullvad.net/media/files/mullvad-wg.sh                                                               #
#  SPDX-License-Identifier: GPL-2.0                                                                                    #
#  Copyright (C) 2016-2018 Jason A. Donenfeld <Jason@zx2c4.com>. All Rights Reserved.                                  #
# -------------------------------------------------------------------------------------------------------------------- #
#  Preforms the following actions:                                                                                     #
#   - Checks for an existing WireGuard VPN connection and if found exits script                                        #
#   - Prompts user for Mullvad account number, user can also choose to skip vpn setup which exits script               #
#   - Registers a new private key for this host with Mullvad account                                                   #
#   - Generates WireGuard configuration files for each VPN endpoint in the preferred region                            #
#   - Randomly selects one of the generated configuration files and starts the VPN service using it                    #
########################################################################################################################

DNS_SERVER="193.138.218.74"
PREFERRED_COUNTRY="USA"
PRIVATE_KEY="$(wg genkey)"
SKIP_STRING="skip"
WIREGUARD_CONFIG_DIR="/etc/wireguard"

declare -A SERVER_ENDPOINTS
declare -A SERVER_PUBLIC_KEYS
declare -a SERVER_CODES

# Set pipe fail
set -e

# Verify curl and jQuery are installed
exec_exists "curl"
exec_exists "jq"

# Check for an active WireGuard VPN connection, exit now if one is found
print_header "Checking for active VPN connection"
if systemctl list-units --type=service --state=active,running | awk '/.*\.service/ {print $1}' | grep wg-quick@; then
    echo "VPN connection is active, no additional setup required"
    exit 0
else
    echo "No VPN connection active, will prompt for setup"
fi

# Prompt for Mullvad account number
print_header "Prompting for VPN credentials"
while :; do
    echo "This script can setup a WireGuard connection to Mullvad VPN automatically."
    echo "If you want to setup a VPN connection now, enter your Mullvad account number below."
    echo "If you DO NOT want to set up a VPN connection, enter '$SKIP_STRING' instead."
    read -p "> " -r ACCOUNT

    # If user asked to skip, exit now
    if [[ "$ACCOUNT" == "$SKIP_STRING" ]]; then
        echo "Skipping VPN setup"
        exit 0
    fi

    # Check provided input for valid account number pattern (16 digits), if valid break the loop and continue script
    if echo "$ACCOUNT " | grep "[0-9]\{16\} " &>/dev/null; then
        echo "Account number '$ACCOUNT' appears to be valid, attempting setup"
        break
    else
        echo "Account number '$ACCOUNT' does not appear to be valid, please try again"
        echo
    fi
done

# Register private key with Mullvad API
echo "Submitting keys to Mullvad API"
RESPONSE="$(curl -sSL https://api.mullvad.net/wg/ -d account="$ACCOUNT" --data-urlencode pubkey="$(wg pubkey <<<"$PRIVATE_KEY")")" || error_exit "Could not talk to Mullvad API"
[[ $RESPONSE =~ ^[0-9a-f:/.,]+$ ]] || error_exit "$RESPONSE"
ADDRESS="$RESPONSE"

# Query Mullvad API for endpoint info
print_header "Generating WireGuard configuration files for Mullvad VPN"
echo "Querying Mullvad API for VPN endpoint info"
RESPONSE="$(curl -LsS https://api.mullvad.net/public/relays/wireguard/v1/)" || error_exit "Unable to connect to Mullvad API"
FIELDS="$(jq -r 'foreach .countries[] as $country (.; .; foreach $country.cities[] as $city (.; .; foreach $city.relays[] as $relay (.; .; $country.name, $city.name, $relay.hostname, $relay.public_key, $relay.ipv4_addr_in)))' <<<"$RESPONSE")" || error_exit "Unable to parse response"
while read -r COUNTRY && read -r CITY && read -r HOSTNAME && read -r PUBKEY && read -r IPADDR; do
    if [[ "$COUNTRY" != "$PREFERRED_COUNTRY" ]]; then
        continue
    fi
	CODE="${HOSTNAME%-wireguard}"
	SERVER_CODES+=( "$CODE" )
	SERVER_PUBLIC_KEYS["$CODE"]="$PUBKEY"
	SERVER_ENDPOINTS["$CODE"]="$IPADDR:51820"
done <<<"$FIELDS"

# Create the WireGuard config dir if it does not exist
if [[ ! -d "$WIREGUARD_CONFIG_DIR" ]]; then
    sudo mkdir -p "$WIREGUARD_CONFIG_DIR"
fi

# Generate WireGuard configuration files
echo "Writing Mullvad VPN endpoint info to WireGuard configuration files"
for CODE in "${SERVER_CODES[@]}"; do
	CONFIGURATION_FILE="$WIREGUARD_CONFIG_DIR/$CODE.conf"
	umask 077
	sudo rm -f "$CONFIGURATION_FILE.tmp"
	sudo tee -a "$CONFIGURATION_FILE.tmp" > /dev/null <<- EOF
		[Interface]
		PrivateKey = $PRIVATE_KEY
		Address = $ADDRESS
		DNS = $DNS_SERVER

		[Peer]
		PublicKey = ${SERVER_PUBLIC_KEYS["$CODE"]}
		Endpoint = ${SERVER_ENDPOINTS["$CODE"]}
		AllowedIPs = 0.0.0.0/0, ::/0
	EOF
	sudo mv "$CONFIGURATION_FILE.tmp" "$CONFIGURATION_FILE"
done

# Randomly select a WireGuard configuration and enable it
print_header "Enabling Mullvad VPN WireGuard service"
RANDOM_CODE=${SERVER_CODES[ $RANDOM % ${#SERVER_CODES[@]} ]}
sudo systemctl --now enable "wg-quick@$RANDOM_CODE"

exit 0
