# check if arch is X86_64
A = arch
A == ARCH_X86_64 ? next : dead
A = sys_number
A >= 0x40000000 ? dead : next
A == fstat ? ok : next
A == openat ? ok : next
A == write ? ok : next
A == exit ? ok : next
A == exit_group ? ok : next
A == mprotect ? ok : next
A == mmap ? ok : next
A == munmap ? ok : next
A == brk ? ok : next
A == close ? ok : next
dead:
return KILL
ok:
return ALLOW
