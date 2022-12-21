#!/usr/bin/env python3

from pwn import *
import subprocess

HOST = "34.83.179.82"
PORT = 30263

def POW():
    r.recvuntil(b"token:\n")
    cmd = r.recvline().strip()
    token = subprocess.check_output(cmd, shell=True).strip()
    log.success("token: {}".format(token))
    r.sendline(token)

if __name__ == "__main__":

    r = remote(HOST, PORT)
    # POW & send HTML
    POW()
    html = open(sys.argv[1], "rb").read()
    sz = len(html)
    assert sz <= 10*1024
    log.success("file size: {}".format(sz))
    r.sendlineafter(b"size:", str(sz).encode())
    r.sendafter(b"file:", html)

    r.interactive()
