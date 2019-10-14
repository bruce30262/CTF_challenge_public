#ifndef VM_H_
#define VM_H_

#include <bits/stdc++.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    NOP = 1,
    ADD,
    SUB,
    MUL,
    MOD,
    XOR,
    AND,
    LT , // less then
    EQ , // equal
    BR , // branch
    BRT, // branch if true
    BRF, // branch if false
    PUSH, 
    POP, 
    LD, // load
    ST, // store
    NEW, // new
    DEL, // delete
    RB, // read buf
    WB, // write buf
    PSTK, // print stack
    PN, // print number
    HLT   //over
}INST;

#ifdef __cplusplus
}
#endif

void InitVM();
int ExecVM(std::wstring& src);

#endif
