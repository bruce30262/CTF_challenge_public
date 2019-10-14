#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

// flag == hitcon{tH4nK_U_s0_muCh_F0r_r3c0v3r1ng_+h3_fL4g_1_Luv_y0u_<3}

int my_strlen(char *str) {
    int ret = 0;
    char *c = str;
    while(*c != 0){
        c++;
        ret++;
    }
    return ret;
}

void my_strncpy(char *dst, char *src, int len) {
    char *c = dst;
    int i = 0;
    for(i = 0 ; i < len ; i++) {
        *c++ = *src++;
    }
}

void clear(char *buf, int sz) {
    int i = 0;
    for(i = 0 ; i < sz ; i++) {
        buf[i] = 0;
    }
}

void fail() {
    puts(":(");
    exit(0);
}

int check1(char *buf, int sz) {
    /* simple xor/sub */
    char dumb[] = "DuMb";
    char check[30] = {};
    char answer[] = "\x49\x26\x72\x35\x76\x31\x13\x04\x4e\x5e";
    int i = 0;
    int ok = 1;
    for(i = 0 ; i < sz ; i++) {
        check[i] = (char)((((int)buf[i] & 0xff) ^ (int)dumb[i % 4] - 7)&0xff);
    }

    for (i = 0 ; i < sz ; i++) {
        if( check[i] != answer[i] ) {
            ok = 0;
        }
    }
    return ok;
}

int check2(char *buf) {
    /* xtea */
    uint32_t v0 = 0, v1= 0;
    int idx = 0;
    int ok = 1;
    uint32_t answer[8] = {0x95cb8dbd,0xf84cc79, 0xb899a876,0xa5dab55, 0x9a8b3bba,0x70b238a7, 0x72b53cf1,0xd47c0209};
    for(idx = 0 ; idx < 4 ; idx++) {
        v0 = (uint32_t)(buf[idx]) & 0xff;
        v1 = (uint32_t)(buf[idx+4]) & 0xff;
        uint32_t sum = 0;
        uint32_t delta = 0x1337dead;
        uint32_t key[4] = {67, 48, 82, 51};

        int i = 0;
        for (i=0; i < 32; i++) {
            v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
            sum += delta;
            v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        }                       
        if (v0 != answer[idx*2]) ok = 0;
        if (v1 != answer[idx*2+1]) ok = 0;
    }
    return ok;
}

int check3(char *buf, int sz) {
    /* custom base 64 */
    unsigned char *pos, *end, *in;
    unsigned char out[50]={};
    const char base64_table[65] = "\x2a\x7c\x2d\x49\x66\x6e\x71\x32\x30\x21\x20\x0a\x41\x5a\x64\x24\x72\x3c\x58\x6f\x5c\x44\x2f\x7b\x4b\x43\x7e\x61\x34\x54\x7a\x37\x29\x59\x5e\x3a\x78\x60\x0b\x7d\x53\x73\x31\x79\x4f\x6d\x69\x76\x23\x0d\x25\x5d\x40\x5b\x5f\x4e\x28\x48\x6a\x2c\x56\x51\x75\x67";
    char answer[]="\x34\x60\x51\x25\x41\x5f\x41\x23\x54\x3a\x5a\x25\x41\x2f\x48\x7d\x7b\x25\x6d\x53\x41\x5b\x51\x0b";
    int ok = 1;

    end = buf + sz;
    in = buf;
    pos = out;
    while (end - in >= 3) {
        *pos++ = base64_table[in[0] >> 2];
        *pos++ = base64_table[((in[0] & 0x03) << 4) | (in[1] >> 4)];
        *pos++ = base64_table[((in[1] & 0x0f) << 2) | (in[2] >> 6)];
        *pos++ = base64_table[in[2] & 0x3f];
        in += 3;
    }

    int i = 0;
    for(i = 0 ; i < 24 ; i++) {
        if(out[i] != answer[i]) ok = 0;
    }
    return ok;
}

int check4(char* buf, int sz) {
    /* custom RC4 */
    int S[250]={};
    unsigned char key[] = "Pl3as_d0n\'t_cR45h_1n_+h!s_fUnC+10n";
    unsigned char out[50] = {};
    unsigned char answer[] = "\x2B\x55\x5D\x93\xA0\x43\xDD\x14\x43\x52\x7D\xE5";
    int len = 34;
    int i = 0, j = 0;
    int ok = 1;

    for(i = 0; i < 246; i++) S[i] = i;

    for(i = 0; i < 246; i++) {
        j = (j + S[i] + key[i % len] ) % 246;
        int tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;
    }

    int n = 0;
    i = 0, j = 0;
    while ( n < sz ) {
        i = (i + 1) % 246;
        j = (j + S[i]) % 246;

        int tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;

        int rnd = S[(S[i] + S[j]) % 246];
        out[n] = (unsigned char)(rnd ^ buf[n]);
        n++;
    }

    for(i = 0 ; i < sz ; i++) {
        if(out[i] != answer[i]) ok = 0;
    }
    return ok;
}

int check5(char *buf) {
    /* crc32 */
    int i = 0, j = 0, idx = 0;
    int ok = 1;
    unsigned int byte = 0, crc = 0, mask = 0;

    crc = 0xFFFFFFFF;
    while (buf[i] != 0) {
        byte = buf[i++];
        crc = crc ^ byte;
        for (j = 7; j >= 0; j--) {
            mask = -(crc & 1);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
    }
    if (~crc != 0xd666fed6) ok = 0;
    return ok;
}

int test() {
    asm(".intel_syntax noprefix");
    asm("xor rax, rax");
    asm("mov rax, 0x1337");
    asm(".att_syntax prefix"); 
}

int main(int argc, char *argv[])
{
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);

    char flag[60]={};
    char in[60]={};
    char out[60]={};
    char *c = flag;
    int i = 0;

    if (test() != 0x1337) {
        puts("Test failed !");
        return 1;
    }

    printf("Please enter the flag: ");
    read(0, flag, 55);
    while(*c != 0) {
        if (*c == '\n' || *c == '\r') {
            *c = '\0';
            break;
        }
        c++;
    }
    if(my_strlen(flag) != 52) fail();

    my_strncpy(in, flag, 10);
    if(!check1(in, 10)) fail();

    clear(in, 55);
    my_strncpy(in, &flag[10], 8);
    if(!check2(in)) fail();
    
    clear(in, 55);
    my_strncpy(in, &flag[18], 18);
    if(!check3(in, 18)) fail();
    
    clear(in, 55);
    my_strncpy(in, &flag[36], 12);
    if(!check4(in, 12)) fail();
    
    clear(in, 55);
    my_strncpy(in, &flag[48], 4);
    if(!check5(in)) fail();
    
    printf("Congratz ! The flag is hitcon{%s} :)\n", flag);
    return 0;
}
