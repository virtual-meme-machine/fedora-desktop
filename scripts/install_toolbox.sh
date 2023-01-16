#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  install_toolbox.sh                                                                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
#  Based on 'jetbrains-toolbox.sh'                                                                                     #
#  Source: https://github.com/nagygergo/jetbrains-toolbox-install                                                      #
#  SPDX-License-Identifier: MIT License                                                                                #
#  Copyright (c) 2016 Gergely Nagy                                                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
#  Preforms the following actions:                                                                                     #
#   - Checks if JetBrains Toolbox is installed, if so exits immediately                                                #
#   - Gets the latest JetBrains Toolbox archive URL                                                                    #
#   - Downloads and extracts archive to /opt                                                                           #
#   - Symlinks the JetBrains Toolbox exec to /usr/local/bin                                                            #
#   - Starts JetBrains Toolbox so that it can set itself up                                                            #
########################################################################################################################

BIN_EXEC="/usr/local/bin/jetbrains-toolbox"
TEMP_DIR=$(mktemp -d)
TOOLBOX_DIR="/opt/jetbrains-toolbox"
TOOLBOX_EXEC="$TOOLBOX_DIR/jetbrains-toolbox"
USER_AGENT="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

# Check if JetBrains Toolbox is installed, if so exit now
print_header "Installing JetBrains Toolbox"
if [[ -f "$BIN_EXEC" ]] && [[ -f "$TOOLBOX_EXEC" ]]; then
    echo "JetBrains Toolbox appears to be installed, skipping"
    exit 0
fi

# Query JetBrains website for latest version of Jetbrains Toolbox
echo "Querying JetBrains API for Toolbox download url"
download_url=$(curl 'https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release' -H 'Origin: https://www.jetbrains.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H "${USER_AGENT[@]}" -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://www.jetbrains.com/toolbox/download/' -H 'Connection: keep-alive' -H 'DNT: 1' --compressed | grep -Po '"linux":.*?[^\\]",' | awk -F ':' '{print $3,":"$4}'| sed 's/[", ]//g')
base_file=$(basename "$download_url")
download_path="$TEMP_DIR/$base_file"

# Download JetBrains Toolbox archive
echo "Downloading JetBrains Toolbox archive '$base_file'"
if ! wget -cO "$download_path" "$download_url" --read-timeout=5 --tries=0 &>/dev/null; then
    error_exit "Failed to download JetBrains Toolbox"
fi

# Create JetBrains Toolbox directory
if [[ ! -d "$TOOLBOX_DIR" ]]; then
    echo "Creating JetBrains Toolbox directory at '$TOOLBOX_DIR'"
    if ! sudo mkdir -p "$TOOLBOX_DIR"; then
        error_exit "Failed to create JetBrains Toolbox directory"
    fi
fi

# Extract JetBrains Toolbox archive
echo "Extracting JetBrains Toolbox archive to '$TOOLBOX_DIR'"
if ! sudo tar -xzf "$download_path" -C "$TOOLBOX_DIR" --strip-components=1; then
    error_exit "Failed to extract JetBrains Toolbox archive"
fi

# Create a symlink to the exec so that we can access it
echo "Symlinking JetBrains Toolbox exec to '$BIN_EXEC'"
sudo rm -rf "$BIN_EXEC"
if ! sudo ln -s "$TOOLBOX_EXEC" "$BIN_EXEC"; then
    error_exit "Failed to symlink JetBrains Toolbox exec"
fi

# Update permissions on exec and symlink
echo "Setting permissions on JetBrains Toolbox exec"
sudo chmod +rwx "$TOOLBOX_EXEC"
sudo chmod +rwx "$BIN_EXEC"

# Run JetBrains Toolbox so that it sets itself up
echo "Starting JetBrains Toolbox"
if ! "$BIN_EXEC"; then
    error_exit "Failed to start JetBrains Toolbox"
fi

exit 0
