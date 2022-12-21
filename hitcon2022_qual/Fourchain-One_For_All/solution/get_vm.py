#!/usr/bin/env python3

from pwn import *
import subprocess

HOST = "34.168.149.109"
PORT = 31337

def POW2():
    print("POW2...")
    flags = b""
    with open("all_flag.txt", "rb") as f:
        flags = f.read()

    import hashlib
    m = hashlib.sha256()
    m.update(flags)

    r.sendlineafter(b":", m.hexdigest().encode())

def POW1():
    print("POW1...")
    r.recvuntil(b"token:\n")
    cmd = r.recvline().strip()
    token = subprocess.check_output(cmd, shell=True).strip()
    log.success("token: {}".format(token))
    r.sendline(token)

if __name__ == "__main__":

    r = remote(HOST, PORT)
    POW1()
    POW2()
    r.interactive()
