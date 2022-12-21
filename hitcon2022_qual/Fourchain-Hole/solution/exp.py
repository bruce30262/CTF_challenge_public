#!/usr/bin/env python3

from pwn import *
import sys

HOST = "35.227.151.88"
PORT = 30262

def POW():
    r.recvuntil(b"token:\n")
    cmd = r.recvline().strip()
    token = subprocess.check_output(cmd, shell=True).strip()
    log.success("token: {}".format(token))
    r.sendline(token)

if __name__ == "__main__":

    r = remote(HOST, PORT)
    # POW & send JS file
    POW()
    js = open(sys.argv[1], "rb").read()
    sz = len(js)
    assert sz <= 2000
    log.success("file size: {}".format(sz))
    r.sendlineafter(b"size:", str(sz).encode())
    r.sendafter(b"file:", js)

    r.interactive()
