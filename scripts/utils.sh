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