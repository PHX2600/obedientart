#!/usr/bin/env bash

sudo apt-get install -y python python-dev python-virtualenv mysql-server-5.6 libmysqlclient-dev libffi-dev

venv=$HOME/obedientart_virtualenv

virtualenv $venv

$venv/bin/python setup.py develop

mysql -u root -p < <(cat <<EOF
create database obedientart;
CREATE USER 'debug'@'localhost' IDENTIFIED BY 'debug';
GRANT ALL PRIVILEGES ON * . * TO 'debug'@'localhost';
EOF
)
