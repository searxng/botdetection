# SPDX-License-Identifier: AGPL-3.0-or-later

# shellcheck disable=SC2034
terminal.colors() {
    # https://en.wikipedia.org/wiki/ANSI_escape_code

    # CSI (Control Sequence Introducer) sequences
    _show_cursor='\e[?25h'
    _hide_cursor='\e[?25l'

    # SGR (Select Graphic Rendition) parameters
    _creset='\e[0m'  # reset all attributes

    # original specification only had 8 colors
    _colors=8

    _Black='\e[0;30m'
    _White='\e[1;37m'
    _Red='\e[0;31m'
    _Green='\e[0;32m'
    _Yellow='\e[0;33m'
    _Blue='\e[0;94m'
    _Violet='\e[0;35m'
    _Cyan='\e[0;36m'

    _BBlack='\e[1;30m'
    _BWhite='\e[1;37m'
    _BRed='\e[1;31m'
    _BGreen='\e[1;32m'
    _BYellow='\e[1;33m'
    _BBlue='\e[1;94m'
    _BPurple='\e[1;35m'
    _BCyan='\e[1;36m'
}

if [ ! -p /dev/stdout ] && [ ! "${TERM}" = 'dumb' ] && [ ! "${TERM}" = 'unknown' ]; then
    terminal.colors
fi

