#!/usr/bin/env python3

# ./find_symbolic_x0.py <bin_path> <vfs.json>

import angr
import claripy
import sys
import json
import logging

logging.getLogger('cle').setLevel(logging.ERROR)

def analyze_func(binary_path, func_addr):
    print(f"************** Trying function: {hex(func_addr)} ********************")
    proj = angr.Project(binary_path, main_opts={'base_addr': 0}, auto_load_libs=False)

    ret_addr = 0x18B8C
    buf_size = 0x40
    buf_addr = 0x100000
    sym_buf = claripy.BVS("sym_buf", buf_size * 8)

    # set state, x0 points to sym_buf
    state = proj.factory.call_state(addr=func_addr, ret_addr=ret_addr)
    state.regs.x0 = buf_addr
    state.memory.store(buf_addr, sym_buf)

    # detect symbolic read
    symbolic_reads = []
    def mem_read_callback(state):
        read_addr = state.inspect.mem_read_address
        if state.solver.symbolic(read_addr):
            symbolic_reads.append((state.addr, read_addr))
            #print(f"[+] Symbolic read at 0x{state.addr:x}, from addr: {read_addr}")

    # inspect memory read
    state.inspect.b("mem_read", when=angr.BP_BEFORE, action=mem_read_callback)
    # explore
    simgr = proj.factory.simgr(state)
    simgr.explore(find=lambda s: s.addr == ret_addr, n=1000)

    # show symbolic reads info
    if symbolic_reads:
        print(f"\n[+] Function at 0x{func_addr:x} performs symbolic reads:")
        for addr, raddr in symbolic_reads:
            print(f"\tAt 0x{addr:x}, read from symbolic addr: {raddr}")
    else:
        print(f"\n[-] Function at 0x{func_addr:x} does not perform symbolic reads")
        return
    # show symbolic X0 info
    if simgr.found:
        for found in simgr.found:
            retval = found.regs.x0
            if found.solver.symbolic(retval):
                print(f"[+] Function at 0x{func_addr:x} has symbolic X0: {retval}")

    """
    print("Active states:", simgr.active)
    print("Deadended states:", simgr.deadended)
    print("Errored states:")
    for e in simgr.errored:
        print(f"  Error at {e.state.addr:#x}: {e.error}")
    """

if __name__ == '__main__':
    binary_path = sys.argv[1]
    vfs_json = sys.argv[2]
    func_list = None
    with open(vfs_json, "r") as f:
        func_list = json.load(f)

    skip = [0x1bde8]
    for idx, f in enumerate(func_list):
        print(f"{idx+1}/{len(func_list)}: {hex(f)}")
        sys.stdout.flush()
        if f not in skip:
            analyze_func(binary_path, f)
        else:
            print(f"[-] Skip {hex(f)}")

