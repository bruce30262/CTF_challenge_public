#!/usr/bin/python3 -u

import atexit
import binascii
import os
import pwd
import random
import signal
import string
import sys

BIN_PATH = b"/home/ctf/run.sh"
FILE_DIR = b"/opt/files/"
MAX_INPUT = 2000
TIMEOUT = 120

filename = FILE_DIR + binascii.hexlify(os.urandom(10))

def handle_exit(*args):
    global filename
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except:
        pass
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

def POW():
    from hashcash import check
    bits = 25
    resource = "".join(random.choice(string.ascii_lowercase) for i in range(8))
    print("[POW] Please execute the following command and submit the hashcash token:")
    print("hashcash -mb{} {}".format(bits, resource))
    print("( You can install hashcash with \"sudo apt-get install hashcash\" )")
    print("hashcash token: ", end='')
    sys.stdout.flush()

    stamp = sys.stdin.readline().strip()

    if not stamp.startswith("1:"):
        print("Only hashcash v1 supported")
        return False

    if not check(stamp, resource=resource, bits=bits):
        print("Invalid")
        return False

    return True

def main():
    global filename
    size = None
    try:
        print(f"Your javscript file size: ( MAX: {MAX_INPUT} bytes ) ", end='')
        size = int(sys.stdin.readline())
    except:
        print("Not a valid size !")
        return

    if size > MAX_INPUT:
        print("Too large !")
        return

    print("Input your javascript file:")
    js = sys.stdin.read(size)

    with open(filename, "wb") as f:
        f.write(js.encode())

    child_pid = os.fork()
    if child_pid == 0:
        # Dropping privilege
        _, _, uid, gid, _, _, _ = pwd.getpwnam("ctf")
        os.setgid(gid)
        os.setuid(uid)
        # launch d8
        os.execv(BIN_PATH, [BIN_PATH, filename])
    else:
        pid, status = os.waitpid(child_pid, 0)
        handle_exit()

if __name__ == '__main__':
    try:
        init()
        if POW():
            main()
        else:
            print("POW failed !")
    except Exception as e:
        pass
