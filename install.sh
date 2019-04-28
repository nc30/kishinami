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
fi
sudo cp ${SCRIPT_DIR}/run.py ${APP}/
python3 ${SCRIPT_DIR}/setup.py sdist
FILE=$(ls dist/|head -n 1)
sudo ${APP}/python/bin/pip3 install ${SCRIPT_DIR}/dist/${FILE}

[ ! -e /etc/systemd/system/kishinami.service ] && sudo cp ${SCRIPT_DIR}/kishinami.service /etc/systemd/system/

exit 0