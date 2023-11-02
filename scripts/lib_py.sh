# SPDX-License-Identifier: AGPL-3.0-or-later

_REQUIREMENTS=( "${_REQUIREMENTS[@]}" python)
PY_VENV="${PRJ_ROOT-.}/.venv"

py.help(){
    cat <<EOF
py.:
  clean     : clean up python environment and remnants
  env.:
    activate: python virtual environment
    build   : build python virtual environment ($PY_VENV)
    drop    : remove $PY_VENV
EOF
}

py.clean() {
    msg.build CLEAN "clean up python environment and remnants"
    (   set -e
        py.env.drop
        rm -rf ./.tox ./*.egg-info
        find . -name '*.pyc' -exec rm -f {} +
        find . -name '*.pyo' -exec rm -f {} +
        find . -name __pycache__ -exec rm -rf {} +
    )
}

py.env.activate() {
    # shellcheck source=/dev/null
    . "${PY_VENV}/bin/activate"
}

py.env.build() {
    msg.build ENV "build ${PY_VENV}"
    # https://docs.python.org/3/library/venv.html
    python -m venv "$PY_VENV"
    "${PY_VENV}/bin/python" -m pip install --upgrade pip
}

py.env.drop() {
    msg.build CLEAN "remove ${PY_VENV}"
    rm -rf "${PY_VENV}"
}
