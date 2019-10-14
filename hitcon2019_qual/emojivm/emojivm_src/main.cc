#include <bits/stdc++.h>
#include <unistd.h>
#include <signal.h>
#include "vm.h"

#include <linux/seccomp.h>
#include <sys/prctl.h>

#define TIMEOUT 60

using namespace std;

wstring LoadSrc(const char* path) {
    /* Load source file and convert it to wstring */
    auto ss = ostringstream{};
    ifstream file(path);
    ss << file.rdbuf();
    using convert_typeX = codecvt_utf8<wchar_t>;
    wstring_convert<convert_typeX, wchar_t> converterX;
    return converterX.from_bytes(ss.str());
}

#ifdef SECCOMP
static void install_seccomp() {
    // generate by seccomp-tools: https://github.com/david942j/seccomp-tools
    static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,12,62,0,0,192,32,0,0,0,0,0,0,0,53,0,10,0,0,0,0,64,21,0,10,0,5,0,0,0,21,0,9,0,1,1,0,0,21,0,8,0,1,0,0,0,21,0,7,0,60,0,0,0,21,0,6,0,231,0,0,0,21,0,5,0,10,0,0,0,21,0,4,0,9,0,0,0,21,0,3,0,11,0,0,0,21,0,2,0,12,0,0,0,21,0,1,0,3,0,0,0,6,0,0,0,0,0,0,0,6,0,0,0,0,0,255,127};
    struct prog {
        unsigned short len;
        unsigned char *filter;
    } rule = {
        .len = sizeof(filter) >> 3,
        .filter = filter
    };
    if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) { perror("prctl(PR_SET_NO_NEW_PRIVS)"); exit(2); }
    if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) { perror("prctl(PR_SET_SECCOMP)"); exit(2); }
}
#endif

void stop(int signum) {
    wcout << "TIMEOUT !" << endl;
    exit(1);
}

void init() {
    setlocale(LC_ALL, "en_US.utf8");
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    signal(SIGALRM, stop);
    alarm(TIMEOUT);
}

int main(int argc, char *argv[]) {
    if(argc != 2) {
        puts("Usage: ./emojivm <source_file>");
        exit(1);
    }
    init();
    InitVM();
    wstring src = LoadSrc(argv[1]);
#ifdef SECCOMP
    install_seccomp();
#endif
    int ret = ExecVM(src);
#ifdef DEBUG
    wcout << "ret: " << ret << endl;
#endif
    return ret;
}    
