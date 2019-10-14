#!/usr/bin/env python
import sys

names = ["check1", "check2", "check3", "check4", "check5", "test"]

for name in names:
    code= ""
    infile = name + ".enc"
    with open(infile, "rb") as f:
        code = f.read()
    print "\n========================{}==============================\n".format(infile)
    print "len:", len(code)
    for c in code:
        sys.stdout.write("\\x{:02x}".format(ord(c)))
    print
