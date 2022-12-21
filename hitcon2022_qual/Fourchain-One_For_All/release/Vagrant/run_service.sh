#!/bin/bash
exec 2>/dev/null
timeout --foreground -k 1 600 /home/vagrant/service.py
