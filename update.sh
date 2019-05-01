#!/bin/bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
APP=/opt/kishinami

sudo cp ${SCRIPT_DIR}/run.py ${APP}/
sudo rm -rf ${SCRIPT_DIR}/kishinami.egg-info
python3 ${SCRIPT_DIR}/setup.py sdist
FILE=$(ls dist/|tail -n 1)
sudo ${APP}/python/bin/pip3 install --upgrade --force ${SCRIPT_DIR}/dist/${FILE}

[ ! -e /etc/systemd/system/kishinami.service ] && sudo cp ${SCRIPT_DIR}/kishinami.service /etc/systemd/system/

exit 0
