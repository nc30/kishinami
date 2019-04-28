#!/bin/bash

set -E

SCRIPT_DIR=$(cd $(dirname $0); pwd)
APP=/opt/kishinami

which python3 > /dev/null || sudo apt-get install python3 -y
which pip > /dev/null || sudo apt-get install python3-pip -y
which virtualenv > /dev/null || sudo apt-get install python3-virtualenv -y

if [ ! -d ${APP} ]; then
    sudo mkdir ${APP}
    cd ${APP}
    sudo virtualenv python --python=$(which python3)
    sudo ${APP}/python/bin/pip3 install ${SCRIPT_DIR}
    sudo cp ${SCRIPT_DIR}/run.py ${APP}/
fi

if [ ! -e /etc/systemd/system/kishinami.service ]; sudo cp ${SCRIPT_DIR}/kishinami.service /etc/systemd/system/

exit 0