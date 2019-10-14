#!/usr/bin/python -u
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import tempfile
import sys, os, random, string, signal, atexit
from hashlib import sha256

FLAG = "hitcon{M0mmy_I_n0w_kN0w_h0w_t0_d0_9x9_em0j1_Pr0gr4mM!ng}"
BIN_PATH = "/opt/emojivm"
LOG_DIR = "/opt/log/"
CORRECT_ANSWER_FILE = "/opt/answer"
MAX_INPUT = 2000
TIMEOUT = 120

filename = None
correct_answer = ""

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
    global correct_answer, CORRECT_ANSWER_FILE
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(TIMEOUT)
    with open(CORRECT_ANSWER_FILE, "rb") as f:
        correct_answer = f.read()

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

    if '📄' in emoji:
        print("You don't need to read stuff in this challenge !")
        return

    f = tempfile.NamedTemporaryFile(prefix='', delete=False)
    f.write(emoji)
    f.close()
    filename = f.name

    cmd = "timeout -k 5 10 {} {}".format(BIN_PATH, filename)
    output = ""
    evil = [159, 139, 134, 132] # SIGSYS, SIGSEGV, SIGABRT, SIGILL
    ret = None
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as grepexc:
        ret = grepexc.returncode
        if ret in evil:
            print("Woah! Hold your horses buddy !")
            print("You might want to keep that for \"another\" challenge ;)")
        elif ret == 1:
            print(grepexc.output)
        else:
            print("Program exit with code:{}".format(ret))
        handle_exit()

    if output == correct_answer:
        print("Good job ! Here's the flag:\n{}".format(FLAG))
    else:
        print("Wrong answer !")

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
