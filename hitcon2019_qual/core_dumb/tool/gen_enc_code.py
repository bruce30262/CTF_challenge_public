#!/usr/bin/env python

import struct 

def p32(x):
    return struct.pack('<I', x & 0xffffffff)

def u32(x):
    return struct.unpack('<I', x.ljust(4, '\x00'))[0]

names = ["check1", "check2", "check3", "check4", "check5", "test"]
keys = [0x8EB5034A, 0xC6FFDA44, 0x85EA3FE1, 0x42AD9EF2, 0x77E2535C, 0x29116162]

for idx, name in enumerate(names):
    out , code= "", ""
    with open(name, "rb") as f:
        code = f.read().strip()
    key = keys[idx]
    ks = p32(key)

    for i, c in enumerate(code):
       out += chr((ord(c) ^ ord(ks[i % 4]))&0xff)
    outfile = "{}.enc".format(name)
    with open(outfile, "wb") as f:
        print("Writing to {}".format(outfile))
        f.write(out)

print "Done"
