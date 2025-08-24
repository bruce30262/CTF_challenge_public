#!/usr/bin/env python3

# ./find_bin_addr.py <bin_path> <vfs.json>

import angr
import claripy
import sys
import json
import logging
import traceback

logging.getLogger('cle').setLevel(logging.ERROR)

def is_addr_in_bin(addr: int, proj: angr.Project) -> bool:
    mainobj = proj.loader.main_object
    return mainobj.min_addr <= addr < mainobj.max_addr

def analyze_x0(binary_path, base_addr, func_addr):
    proj = angr.Project(binary_path, auto_load_libs=False, main_opts={"base_addr": base_addr})

    func_addr += base_addr
    ret_addr = base_addr + 0x18B8C

    state = proj.factory.call_state(addr=func_addr, ret_addr=ret_addr, \
                                    add_options={angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY, \
                                                 angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS })
    # start finding
    simgr = proj.factory.simgr(state)
    simgr.explore(find=lambda s: s.addr == ret_addr, n=1000)

    if simgr.found:
        found = simgr.found[0]
        x0_val = found.regs.x0
        concrete = found.solver.eval(x0_val)
        if is_addr_in_bin(concrete, proj):
            return concrete - base_addr


def detect_bin_addr(binary_path, func_addr):
    base1 = 0
    base2 = 0x400000
    # analyze x0 with base1
    map1 = dict()
    res = analyze_x0(binary_path, base1, func_addr)
    if res:
        map1[func_addr] = res
    # analyze x0 when base2
    map2 = dict()
    res = analyze_x0(binary_path, base2, func_addr)
    if res:
        if map1[func_addr] == res:
            print(f"[!!] Function {hex(func_addr)} set X0 to binary address !")

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
                detect_bin_addr(binary_path, f)
            except:
                print(f"[-] Exception while analyzing {hex(f)}")
                print(traceback.format_exc())
                pass
        else:
            print(f"[-] Skip {hex(f)}")
