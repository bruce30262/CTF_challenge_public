#!/bin/bash
exec 2>/dev/null
timeout -k 1 600 /home/vagrant/chromium/chrome --headless --disable-gpu --remote-debugging-port=9222 --enable-logging=stderr "$1"
