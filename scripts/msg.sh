# SPDX-License-Identifier: AGPL-3.0-or-later

# shellcheck source=./lib_terminal.sh
. /dev/null

msg.info() { echo -e "${_BYellow}INFO:${_creset}  $*" >&2; }
msg.warn() { echo -e "${_BBlue}WARN:${_creset}  $*" >&2; }
msg.err()  { echo -e "${_BRed}ERROR:${_creset} $*" >&2; }

msg.build() {
    local tag="$1        "
    shift
    echo -e "${_Blue}${tag:0:10}${_creset}$*"
}
