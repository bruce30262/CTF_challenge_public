#!/usr/bin/env python

import sys

#answer = "plis-g1v3-me33-th3e-f14g"
#FLAG   = "hitcon{R3vers3_Da_3moj1}"
enc    = list("18051d1042094a24005b081740007230096c5640095b051a".decode('hex'))
op_buf = ["\x00"]*30
check  = list("8e63cd124b5815175122d904512c1915862cd14c842e2006".decode('hex'))

key_buf = ["\x00"]*30
key = raw_input("input secret key:")

# emulate read buf
for i, c in enumerate(key):
    key_buf[i] = c

# calculate len, strip newline
sz = 0
for i, c in enumerate(key_buf):
    if c == "\x00":
        break
    if c == "\n":
        key_buf[i] = "\x00"
        break
    sz += 1
# check len
if sz != 24:
    print("Wrong len")
    exit(0)
# check format
for i in xrange(24):
    if (i+1)%5 == 0:
        c = key_buf[i]
        if c != '-':
            print("Wrong format")
            exit(0)
# operate
for i in xrange(24):
    c = ord(key_buf[i])
    tmp = '\x00'
    if i%4 == 0:
        tmp = c + 30
    elif i%4 == 1:
        tmp = (c - 8) ^ 0x7
    elif i%4 == 2:
        tmp = ((c + 44) ^ 0x44) - 4
    elif i%4 == 3:
        tmp = (c ^ 101) ^ (0xac & 0x14)
    op_buf[i] = chr(tmp)

# verify
cnt = 0
for i in xrange(24):
    if op_buf[i] == check[i]:
        cnt += 1
    else:
        cnt -= 1
# check answer
if cnt == 24:
    for i in xrange(24):
        enc[i] = chr(ord(enc[i])^ord(key_buf[i]))
    print ''.join(enc)
else:
    print(":(")

