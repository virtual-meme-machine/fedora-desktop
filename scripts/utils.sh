#!/usr/bin/env bash
########################################################################################################################
#  utils.sh                                                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #
#  Collection of utility functions shared by the scripts in this package.                                              #
########################################################################################################################

############################################################
#  error_exit()                                            #
#  Prints an error message and then exits.                 #
# -------------------------------------------------------- #
#  [$1] String containing the error message, eg: "Failed"  #
############################################################
function error_exit() {
    tput setaf 1    # Set text color to red
    echo "$1"
    tput sgr0

    exit 1
}

############################################################
#  exec_exists()                                           #
#  Verifies the given exec is available, exits if not.     #
# -------------------------------------------------------- #
#  [$1] Command we are checking for, eg: 'zip'             #
############################################################
function exec_exists() {
    if ! command -v "$1" &>/dev/null; then
        error_exit "'$1' could not be found in a reachable path ('$PATH')"
    fi
}

############################################################
#  print_header()                                          #
#  Prints a large formatted message box.                   #
# -------------------------------------------------------- #
#  [$1] String that should be printed, eg: "Testing 123"   #
############################################################
function print_header() {
    tput setaf 3    # Set text color to yellow
    echo "================================================================================"
    echo -e " ${1}"
    echo "================================================================================"
    tput sgr0
}

############################################################
#  prompt_yes_no()                                         #
#  Prompts the user to answer yes or no.                   #
# -------------------------------------------------------- #
#  [$1] Prompt string, eg: "Would you like do to X?"       #
############################################################
function prompt_yes_no() {
    local answer=""
    while :; do
        read -p "$1 (y/n): " -r answer
        if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
            echo 0
            return
        elif [[ "$answer" == "n" || "$answer" == "N" ]]; then
            echo 1
            return
        fi
    done
}