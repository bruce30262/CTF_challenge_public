#!/usr/bin/env python

from pwn import *
import itertools, string, hashlib, sys, subprocess

HOST = "3.115.122.69"
PORT = 30261

def POW():
    r.recvuntil("token:\n")
    cmd = r.recvline().strip()
    token = subprocess.check_output(cmd, shell=True).strip()
    log.success("token: {}".format(token))
    r.sendline(token)

r = remote(HOST, PORT)
POW()
emo = open(sys.argv[1], "rb").read()
sz = len(emo)
r.sendlineafter("size:", str(sz))
r.sendafter("file:", emo)

r.interactive()
