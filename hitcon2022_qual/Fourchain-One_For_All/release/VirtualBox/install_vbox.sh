#!/bin/sh
sudo apt update
sudo apt install build-essential vagrant libpulse0 libvpx7 linux-headers-amd64 -y
sudo ./vbox.run