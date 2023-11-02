#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later

_REQUIREMENTS=( "${_REQUIREMENTS[@]}" )
_SCRIPTS="$(dirname "${BASH_SOURCE[0]}")"

# shellcheck source=./msg.sh
source "${_SCRIPTS}/msg.sh"
# shellcheck source=.//lib_terminal.sh
source "${_SCRIPTS}/lib_terminal.sh"

main() {

    scripts.requires "${_REQUIREMENTS[@]}"
    local _type
    local cmd="$1"; shift

    if [ "$cmd" == "" ]; then
        help
        msg.err "missing command"
        return 42
    fi

    case "$cmd" in
        --getenv) var="$1"; echo "${!var}";;
        --help) help;;
        --*)
            help
            err_msg "unknown option $cmd"
            return 42
            ;;
        *)
            _type="$(type -t "$cmd")"
            if [ "$_type" != 'function' ]; then
                msg.err "unknown command: $cmd / use --help"
                return 42
            else
                "$cmd" "$@"
            fi
            ;;
    esac
}

scripts.requires() {

    # usage:  main.requires [cmd1 ...]

    local exit_val=0
    while [ -n "${1}" ]; do

        if ! command -v "${1}" &>/dev/null; then
            msg.err "missing command ${1}"
            exit_val=42
        fi
        shift
    done
    return $exit_val
}

scripts.import() {
    # shellcheck source=/dev/null
    source "${_SCRIPTS}/lib_${1}.sh"
}

dump_return() {

    # Use this as last command in your function to prompt an ERROR message if
    # the exit code is not zero.

    local err=$1
    [ "$err" -ne "0" ] && msg.err "${FUNCNAME[1]} exit with error ($err)"
    return "$err"
}
