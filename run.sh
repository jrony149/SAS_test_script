#!/bin/bash

pip3 install requests
#firewall-cmd --permanent --add-masquerade
#firewall-cmd --reload
apt-get update
echo "--------------------BEGINNING REQ/RES TESTS--------------------"
python3 ./src/runTests.py
