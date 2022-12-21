#!/usr/bin/python3 -u
import atexit
import signal
import subprocess
import sys
import os

TIMEOUT = 600

BIN = "/home/vagrant/visit.sh"

ok_str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:/.'

def handle_exit(*args):
    exit(0)

def timeout(signum, frame):
    print("TIMEOUT")
    handle_exit()

def init():
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(TIMEOUT)

def check(url):
    if len(url) > 100 or len(url) == 0 or not (url.startswith("http://") or url.startswith("https://")):
        print("Invalid URL")
        return False
    for c in url:
        if c not in ok_str:
            print("Invalid character: "+c)
            return False
    return True

try:
    print("Give me URL ( MAX length 100 ): ",end='')
    URL = sys.stdin.readline().strip()
    if check(URL):
        print(f"Your URL : {URL}")
        try:
            subprocess.check_call( [BIN] + [URL] )
        except subprocess.CalledProcessError as e:
            print("Execution error:")
            print(f"Return code: {e.returncode}")
        print("Done")
        exit(0)
    else:
        exit(1)
except Exception:
    pass
