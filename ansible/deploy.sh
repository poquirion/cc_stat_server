#!/usr/bin/env bash

# centos dependencies
# sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
# sudo yum -y install python36u  # no need for git if deploy done from remote server



cd $PROJET_DIR

python3.6 -m venv venv
./venv/bin/python setup.py install

sudo useradd le
www

sudo mkdir /var/log/cc_stat_server
sudo chmod 775  /var/log/cc_stat_server/
sudo chgrp lewww /var/log/cc_stat_server
sudo cp systemd/cc_stat_server.service  /etc/systemd/system/.
sudo systemctl enable cc_stat_server.service
sudo systemctl restart cc_stat_server.service
sudo systemctl status cc_stat_server.service
