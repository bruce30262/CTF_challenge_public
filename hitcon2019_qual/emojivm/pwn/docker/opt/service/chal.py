#!/usr/bin/python -u
# -*- coding: utf-8 -*-

from __future__ import print_function
from hashlib import sha256
import sys, os, pwd, random, string, signal, atexit

BIN_PATH = "/home/emojivm/run.sh"
LOG_DIR = "/opt/log/"
FILE_DIR = "/opt/files/"
MAX_INPUT = 1000
TIMEOUT = 120

filename = FILE_DIR + os.urandom(10).encode('hex')

def logerr():
    import traceback
    ID = "{}".format(os.urandom(10).encode('hex'))
    logfile = LOG_DIR + ID + ".log.err"
    with open(logfile, "w") as f:
        traceback.print_exc(file=f)
    print("====================== UH OH ======================")
    print("Oops ! Something went wrong !")
    print("Please contact admin via IRC and provide this ID: {}".format(ID))

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
    exit(0)

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
        print("Your emoji file size: ( MAX: {} bytes ) ".format(MAX_INPUT), end='')
        size = int(sys.stdin.readline())
    except:
        print("Not a valid size !")
        return

    if size > MAX_INPUT:
        print("Too large !")
        return

    print("Input your emoji file:")
    emoji = sys.stdin.read(size)

    with open(filename, "wb") as f:
        f.write(emoji)

    child_pid = os.fork()
    if child_pid == 0:
        # Dropping privilege
        _, _, uid, gid, _, _, _ = pwd.getpwnam("emojivm")
        os.setgid(gid)
        os.setuid(uid)
        # launch emojivm
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
    except Exception:
        logerr()
        handle_exit()
