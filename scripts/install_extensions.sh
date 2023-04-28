#!/usr/bin/env bash

source "scripts/utils.sh"

########################################################################################################################
#  install_extensions.sh                                                                                               #
# -------------------------------------------------------------------------------------------------------------------- #
#  Preforms the following actions for each extension in the array below:                                               #
#   - Query Gnome Extensions API for extension version that supports the system's Gnome Shell version                  #
#   - Downloads extension as a zip                                                                                     #
#   - Installs extension                                                                                               #
########################################################################################################################

EXTENSION_IDS=(
    appindicatorsupport@rgcjonas.gmail.com              # AppIndicator and KStatusNotifierItem Support
    background-logo@fedorahosted.org                    # Fedora Background Logo
    blur-my-shell@aunetx                                # Blur my Shell
    caffeine@patapon.info                               # Caffeine
    ding@rastersoft.com                                 # Desktop Icons NG (DING)
    quick-settings-audio-panel@rayzeq.github.io         # Quick Settings Audio Panel
)

EXTENSION_DOWNLOAD_URL="https://extensions.gnome.org/extension-data"
EXTENSION_INFO_URL="https://extensions.gnome.org/extension-info"
GNOME_VERSION=$(gnome-shell --version | grep -oP '\d+\d+')
TEMP_DIR=$(mktemp -d)

# Verify curl, gnome-extensions CLI, and jQuery are installed
exec_exists "curl"
exec_exists "gnome-extensions"
exec_exists "jq"

# Install Gnome extensions
print_header "Installing Gnome Shell extensions"
for extension_id in ${EXTENSION_IDS[*]}; do
    # Check if extension is already installed, skip installation if so
    if gnome-extensions list | grep "$extension_id" &>/dev/null; then
        echo "Extension '$extension_id' is already installed, skipping"
        continue
    fi

    # Query Gnome Extensions API for extension version that supports current Gnome Shell version
    extension_info="$(curl -LsS "$EXTENSION_INFO_URL/?uuid=$extension_id")" || error_exit "Unable obtain extension info from API"
    supported_extension_version="$(jq '."shell_version_map" | .'\"$GNOME_VERSION\"' | ."version"' <<<"$extension_info")" || error_exit "Unable to parse supported extension version"

    # If no supported extension version could be located, exit now
    if [[ "$supported_extension_version" == "null" ]]; then
        error_exit "Extension '$extension_id' does not support Gnome Shell version $GNOME_VERSION"
    fi

    # Download extension as a zip
    echo "Downloading extension '$extension_id' version $supported_extension_version"
    extension_zip="${extension_id//@/}.v$supported_extension_version.shell-extension.zip"
    download_path="$TEMP_DIR/$extension_zip"
    if ! curl "$EXTENSION_DOWNLOAD_URL/$extension_zip" --output "$download_path"; then
        error_exit "Failed to download extension '$extension_id'"
    fi

    # Install extension zip
    echo "Installing extension '$extension_id' version $supported_extension_version"
    if ! gnome-extensions install "$download_path" --force; then
        error_exit "Failed to install extension '$extension_id'"
    fi
done

exit 0
