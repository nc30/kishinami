#!/bin/bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
APP=/opt/kishinami
LOG=/var/log/kishinami

which python3 > /dev/null || sudo apt-get install python3 -y
which pip > /dev/null || sudo apt-get install python3-pip -y
which virtualenv > /dev/null || sudo pip3 install virtualenv

if [ ! -d ${APP} ]; then
    sudo mkdir ${APP}
    cd ${APP}
    sudo virtualenv python --python=$(which python3)
fi

if [ ! -d ${LOG} ]; then
    sudo mkdir ${LOG}
    sudo chown pi ${LOG}
fi

sudo cp ${SCRIPT_DIR}/run.py ${APP}/
sudo rm -rf ${SCRIPT_DIR}/kishinami.egg-info
sudo ${APP}/python/bin/pip3 install ${SCRIPT_DIR}/

[ ! -e /etc/systemd/system/kishinami.service ] && sudo cp ${SCRIPT_DIR}/kishinami.service /etc/systemd/system/

exit 0