#!/usr/bin/env python3

import sys

vmcode = dict()
vmdata = [""]*11

labels = dict() # {label:pos}
branchs = [] # (pos, type, dest)

vmcode[b'NOP'] = '🈳'
vmcode[b'ADD'] = '➕'
vmcode[b'SUB'] = '➖'
vmcode[b'MUL'] = '❌'
vmcode[b'XOR'] = '❎'
vmcode[b'MOD'] = '❓'
vmcode[b'AND'] = '👫'
vmcode[b'LT'] =  '💀'
vmcode[b'EQ'] =  '💯'
vmcode[b'BR'] =  '🚀'
vmcode[b'BRT'] = '🈶'
vmcode[b'BRF'] = '🈚'
vmcode[b'PUSH'] ='⏬'
vmcode[b'POP'] = '🔝'
vmcode[b'LD'] = '📤'
vmcode[b'ST'] = '📥'
vmcode[b'NEW'] = '🆕'
vmcode[b'DEL'] = '🆓'
vmcode[b'RB'] = '📄'
vmcode[b'WB'] = '📝'
vmcode[b'PSTK'] ='🔡'
vmcode[b'PN'] =  '🔢'
vmcode[b'HLT'] = '🛑'
vmdata[0]='😀'
vmdata[1]='😁'
vmdata[2]='😂'
vmdata[3]='🤣'
vmdata[4]='😜'
vmdata[5]='😄'
vmdata[6]='😅'
vmdata[7]='😆'
vmdata[8]='😉'
vmdata[9]='😊'
vmdata[10]='😍'

def push_num(num):
    if num >= 0 and num <= 10:
        return vmcode[b'PUSH'] + vmdata[num]

    ret = ""
    tmp = abs(num)
    # push digit to stack
    stk = []
    while tmp != 0:
        tens = int(abs(tmp)/10)
        ones = abs(tmp)%10
        tmp = int(tmp/10)
        stk.append(ones)
    # calculate all digit
    # ex. 1234 --> push 1000, 200, 30, 4
    idx = len(stk) - 1
    while idx >= 0:
        now = stk[idx]
        ret += vmcode[b'PUSH'] + vmdata[now]
        for _ in range(idx):
            ret += vmcode[b'PUSH'] + vmdata[10]
            ret += vmcode[b'MUL']
        idx -= 1
    # add all
    for _ in range(len(stk)-1):
        ret += vmcode[b'ADD']

    # if is negative number
    if num < 0:
        ret += vmcode[b'PUSH'] + vmdata[0]
        ret += vmcode[b'SUB']

    return ret

def push_str(s):
    ret = ""
    for c in s[::-1]:
        ret += push_num(c)
    return ret

def store_str(idx, s):
    s += b"\x00"
    ret = push_str(s)
    for i, _ in enumerate(s):
        ret += push_num(i)
        ret += vmcode[b'PUSH'] + vmdata[idx]
        ret += vmcode[b'ST']

    return ret

if len(sys.argv) != 3:
    print("Usage: compiler.py <asm file> <output_file>")
    sys.exit(1)

out = ""
code = open(sys.argv[1], "rb").read().strip().split(b"\n")
for ins in code:
    # comment
    if ins.startswith(b"#") or len(ins.strip()) == 0:
        continue

    ins = ins.strip().split(b" ", 1)
    # this is label
    if b":" in ins[0]:
        k = ins[0].strip().rstrip(b":")
        v = len(out)
        labels[k] = v
        continue
    # handle instruction
    if len(ins) == 1: # single instruction
        out += vmcode[ins[0].upper()]
    elif len(ins) == 2:
        if ins[0].lower() == b"pushstr":
            out += push_str(ins[1].rstrip(b'\"').lstrip(b'\"'))
        elif ins[0].lower() == b"pushnum":
            out += push_num(int(ins[1].strip()))
        elif b"storestr" in  ins[0].lower():
            idx, s = ins[1].strip().split(b" ", 1)
            idx = int(idx)
            s = s.rstrip(b'\"').lstrip(b'\"')
            if b"line" in ins[0].lower():
                s += b'\n'
            elif b"hex" in ins[0].lower():
                import binascii
                s = binascii.unhexlify(s)
            out += store_str(idx, s)
        elif b"br" in ins[0].lower():
            branchs.append((len(out), ins[0].upper(), ins[1].strip()))
            out += "🈳"*45
        else: # push 
            out += vmcode[ins[0].upper()] + vmdata[int(ins[1].strip())]

# handle branch
out = list(out)
for b in branchs:
    pos, ty, dst = b
    dst_pos = labels[dst]
    tmp = push_num(dst_pos) + vmcode[ty]
    cur_pos = pos
    for c in tmp:
        out[cur_pos] = c
        cur_pos += 1

out = "".join(out)

with open(sys.argv[2], "w") as f:
    f.write(out)

print("Done.")

