#include <bits/stdc++.h>
#include <unistd.h>
#include "vm.h"

# define STACK_MAX_SZ 1024
# define BUF_MAX_SZ 1500
# define GPTR_MAX_SZ 10
# define MAX_INS_CNT 1000000

using namespace std;

typedef struct mem{
    size_t sz;
    char *buf;
}MEM;

map<const wchar_t, INST>vmcode;
map<const wchar_t, int>vmdata;
MEM* gptr[GPTR_MAX_SZ];
long stk[STACK_MAX_SZ];

void InitVM() {
    // init vmcode
    vmcode[L'🈳'] = NOP;
    vmcode[L'➕'] = ADD;
    vmcode[L'➖'] = SUB;
    vmcode[L'❌'] = MUL;
    vmcode[L'❓'] = MOD;
    vmcode[L'❎'] = XOR;
    vmcode[L'👫'] = AND;
    vmcode[L'💀'] = LT;
    vmcode[L'💯'] = EQ;
    vmcode[L'🚀'] = BR;
    vmcode[L'🈶'] = BRT;
    vmcode[L'🈚'] = BRF;
    vmcode[L'⏬'] = PUSH;
    vmcode[L'🔝'] = POP;
    vmcode[L'📤'] = LD;
    vmcode[L'📥'] = ST;
    vmcode[L'🆕'] = NEW;
    vmcode[L'🆓'] = DEL;
    vmcode[L'📄'] = RB;
    vmcode[L'📝'] = WB;
    vmcode[L'🔡'] = PSTK;
    vmcode[L'🔢'] = PN;
    vmcode[L'🛑'] = HLT;
    // init vmdata
    vmdata[L'😀'] = 0;
    vmdata[L'😁'] = 1;
    vmdata[L'😂'] = 2;
    vmdata[L'🤣'] = 3;
    vmdata[L'😜'] = 4;
    vmdata[L'😄'] = 5;
    vmdata[L'😅'] = 6;
    vmdata[L'😆'] = 7;
    vmdata[L'😉'] = 8;
    vmdata[L'😊'] = 9;
    vmdata[L'😍'] = 10;
}

int GetData(wchar_t k) {
    if (vmdata.count(k)) return vmdata[k];
    else {
        wcout << "Invalid data code: " << k << endl;
        exit(1);    
    }
}

bool InRange(int low, int up, int cur) {
    if (cur < low) return false;
    if (cur >= up) return false;

    return true;
}

char Load(int idx, int offset) {
    if ( !InRange(0, GPTR_MAX_SZ, idx) || gptr[idx] == nullptr) {
        wcout << "Invalid gptr index" << endl;
        exit(1);
    }
    MEM *tmp = gptr[idx];
    if( !InRange(0, tmp->sz, offset) ) {
        wcout << "Invalid offset detected in LD" << endl;
        exit(1);
    }

    return tmp->buf[offset];
}

void Store(int idx, int offset, char data) {
    if ( !InRange(0, GPTR_MAX_SZ, idx) || gptr[idx] == nullptr) {
        wcout << "Invalid gptr index" << endl;
        exit(1);
    }
    MEM *tmp = gptr[idx];
    if( !InRange(0, tmp->sz, offset) ) {
        wcout << "Invalid offset detected in ST" << endl;
        exit(1);
    }
    tmp->buf[offset] = data;
}

void ReadBuf(int idx) {
    if ( !InRange(0, GPTR_MAX_SZ, idx) || gptr[idx] == nullptr) {
        wcout << "Invalid gptr index" << endl;
        exit(1);
    }
    MEM *tmp = gptr[idx];
    read(0, tmp->buf, tmp->sz);
}

void WriteBuf(int idx) {
    if ( !InRange(0, GPTR_MAX_SZ, idx) || gptr[idx] == nullptr) {
        wcout << "Invalid gptr index" << endl;
        exit(1);
    }
    MEM *tmp = gptr[idx];
    write(1, tmp->buf, strlen(tmp->buf));
}

void PrintStack(int *sp) {
    while(*sp != -1) {
        char c = stk[(*sp)--] & 0xff;
        if (c == '\0') return;
        else write(1, &c, 1);
    }
}

void PrintNum(long num) {
    wcout << num;
}

void DoNew(size_t sz) {
    if ( sz > BUF_MAX_SZ ) {
        wcout << "Invalid size ( too large ) : " << sz << endl;
        exit(1);
    }

    MEM *tmp = new MEM;
    tmp->sz = sz;
    tmp->buf = new char[sz+1];
    memset(tmp->buf, 0, sz+1);

    bool ok = false;
    for (int i = 0; i < GPTR_MAX_SZ; i++) {
        if(gptr[i] == nullptr) {
            gptr[i] = tmp;
            ok = true;
            break;
        }
    }

    if(!ok) {
        delete[]tmp->buf;
        delete tmp;
    }
}

void DoDel(int idx) {
    if ( !InRange(0, GPTR_MAX_SZ, idx) || gptr[idx] == nullptr) {
        wcout << "Invalid gptr index" << endl;
        exit(1);
    }

    MEM *tmp = gptr[idx];
    delete []tmp->buf;
    delete tmp;
    gptr[idx] = nullptr;
}

int ExecVM(wstring& code) {
    int sp = -1;
    int len = code.length();
    int ip = 0;
    long x = 0, y = 0;
    char z = '\0';
    unsigned int ins_cnt = 0;
    while(ip < len) {
        ins_cnt++;
        if (ins_cnt > MAX_INS_CNT) {
            wcout << "Instruction count limit exceeded" << endl;
            exit(1);
        }
        wchar_t c = code[ip];
        switch(vmcode[c])
        {
            case NOP:
                ip++;
#ifdef DEBUG
                wcout << "NOP" << endl;
#endif
                continue;
            case ADD:
                x = stk[sp--];
                y = stk[sp--];
                stk[++sp] = x+y;
                ip++;
#ifdef DEBUG
                wcout << "ADD " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case SUB:
                x = stk[sp--];
                y = stk[sp--];
                stk[++sp] = x-y;
                ip++;
#ifdef DEBUG
                wcout << "SUB " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case MUL:
                x = stk[sp--];
                y = stk[sp--];
                stk[++sp] = x*y;
                ip++;
#ifdef DEBUG
                wcout << "MUL " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case MOD:
                x = stk[sp--];
                y = stk[sp--];
                stk[++sp] = x%y;
                ip++;
#ifdef DEBUG
                wcout << "MOD " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case XOR:
                x = stk[sp--];
                y = stk[sp--];
                stk[++sp] = x^y;
                ip++;
#ifdef DEBUG
                wcout << "XOR " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case AND:
                x = stk[sp--];
                y = stk[sp--];
                stk[++sp] = x&y;
                ip++;
#ifdef DEBUG
                wcout << "AND " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case LT : // less then
                x = stk[sp--];
                y = stk[sp--];
                if ( x < y ) stk[++sp] = 1;
                else stk[++sp] = 0;
                ip++;
#ifdef DEBUG
                wcout << "LT " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case EQ : // equal
                x = stk[sp--];
                y = stk[sp--];
                if ( x == y ) stk[++sp] = 1;
                else stk[++sp] = 0;
                ip++;
#ifdef DEBUG
                wcout << "EQ " << x << " " << y << endl;
                wcout << stk[sp] << endl;
#endif
                break;
            case BR : // branch
                x = stk[sp--];
                ip = x;
#ifdef DEBUG
                wcout << "BR to "<< x << endl;
#endif
                break;
            case BRT: // branch if true
                x = stk[sp--];
                y = stk[sp--];
                if(y) ip = x;
                else ip++; 
#ifdef DEBUG
                wcout << "BRT: "  << "flag: " << y << " pos: "<< ip << endl;
#endif
                break;
            case BRF: // branch if false
                x = stk[sp--];
                y = stk[sp--];
                if(!y) ip = x;
                else ip++; 
#ifdef DEBUG
                wcout << "BRF: "  << "flag: " << !y << " pos: "<< ip << endl;
#endif
                break;
            case PUSH:
                if(sp == STACK_MAX_SZ) {
                    wcout << L"🤮 Stack overflow 🤮" << endl;
                    exit(1);
                }
                x = GetData(code[ip+1]);
                stk[++sp] = x;
                ip += 2;
#ifdef DEBUG
                wcout << "PUSH " << x <<endl;
#endif
                break;
            case POP: 
                if (sp == -1) {
                    wcout << L"😱 Stack underflow 😱" << endl;
                    exit(1);
                }
                sp--;
                ip++;
                break;
            case LD:
                x = stk[sp--]; // idx
                y = stk[sp--]; // offset
                z = Load(x, y);
                stk[++sp] = z;
                ip++;
#ifdef DEBUG
                wcout << "LD " << x << " "<< y << " "<< z <<endl;
#endif
                break;
            case ST:
                x = stk[sp--]; // idx
                y = stk[sp--]; // offset
                z = stk[sp--] & 0xff; // data
                Store(x, y, z);
                ip++;
#ifdef DEBUG
                wcout << "ST " << x << " "<< y << " "<< z <<endl;
#endif
                break;
            case NEW: 
                x = stk[sp--];
                DoNew(x);
                ip++;
#ifdef DEBUG
                wcout << "NEW " << x <<endl;
#endif
                break;
            case DEL:
                x = stk[sp--];
                DoDel(x);
                ip++;
#ifdef DEBUG
                wcout << "DEL " << x <<endl;
#endif
                break;
            case RB:
                x = stk[sp--];
                ReadBuf(x);
                ip++;
                break;
            case WB: 
                x = stk[sp--];
                WriteBuf(x);
                ip++;
                break;
            case PSTK:
                PrintStack(&sp);
                ip++;
                break;
            case PN: 
                x = stk[sp--];
#ifdef DEBUG
                wcout << "PN: ";
#endif
                PrintNum(x);
                ip++;
                break;
            case HLT: 
#ifdef DEBUG
                wcout << "HLT" << endl;
                wcout << "Ins cnt: " << ins_cnt << endl;
#endif
                return 0;
            default:
                wcout << "Invalid opcode: 0x" << hex << int(c) << endl;
                exit(1);    
        }
    }
    return 0;
}

