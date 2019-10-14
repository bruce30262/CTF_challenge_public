addrs = [0x963, 0xa74, 0xc25, 0xf09, 0x12ef, 0x13ae]
names = ["check1", "check2", "check3", "check4", "check5", "test"]
for idx, addr in enumerate(addrs):
    code = ""
    start = idc.get_func_attr(addr, FUNCATTR_START)
    end = idc.get_func_attr(addr, FUNCATTR_END)
    print hex(end - start)
    for ea in xrange(start, end):
        code += chr(Byte(ea))

    with open(names[idx], "wb") as f:
        print "Write to {}".format(names[idx])
        f.write(code)

print "Done"
