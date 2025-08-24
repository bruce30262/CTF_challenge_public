#!/usr/bin/env python3

# ./find_aaw.py <bin_path> <vfs.json>

import angr
import claripy
import sys
import json
import logging
import traceback

logging.getLogger('cle').setLevel(logging.ERROR)

def detect_arbitrary_write(binary_path, func_addr):
    proj = angr.Project(binary_path, auto_load_libs=False, main_opts={"base_addr": 0})

    # set symbolic buffer
    buf_size = 0x40
    buf_addr = 0x100000
    sym_buf = claripy.BVS("sym_buf", buf_size * 8)
    ret_addr = 0x18B8C

    # set states, set X0 points to sym_buf
    state = proj.factory.call_state(addr=func_addr, ret_addr=ret_addr)
    state.regs.x0 = buf_addr
    state.memory.store(buf_addr, sym_buf)

    arbitrary_stores = []

    def mem_write_callback(state):
        addr = state.inspect.mem_write_address
        val = state.inspect.mem_write_expr

        addr_vars = addr.variables # symbolic variable set
        val_vars = val.variables
        buf_vars = sym_buf.variables

        # see if intersect with sym_buf
        addr_related = not addr_vars.isdisjoint(buf_vars)
        val_related  = not val_vars.isdisjoint(buf_vars)

        if addr_related and val_related:
            print(f"[+] Arbitrary write at 0x{state.addr:x} → addr={addr}, val={val}")
            arbitrary_stores.append((state.addr, addr, val))

    # inspect memory write 
    state.inspect.b('mem_write', when=angr.BP_BEFORE, action=mem_write_callback)

    # explore
    simgr = proj.factory.simgr(state)
    simgr.explore(find=lambda s: s.addr == ret_addr, n=1000)

    if arbitrary_stores:
        print(f"\n[!] 🚨 Arbitrary *address* and *value* write detected in function @ 0x{func_addr:x}!")
        for pc, addr, val in arbitrary_stores:
            print(f"  → At 0x{pc:x}: store symbolic value to symbolic address")
    else:
        print(f"\n[-] No arbitrary write detected in function @ 0x{func_addr:x}.")

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
            try:
                detect_arbitrary_write(binary_path, f)
            except:
                print(f"[-] Exception while analyzing {hex(f)}")
                print(traceback.format_exc())
                pass
        else:
            print(f"[-] Skip {hex(f)}")
