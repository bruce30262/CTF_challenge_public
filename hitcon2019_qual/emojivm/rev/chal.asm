# compiler.py chal.asm chal.evm
nop
nop
nop
# banner
pushnum 60
NEW
storestrline 0 "*************************************"
push 0
WB
storestrline 0 "*                                   *"
push 0
WB
storestrline 0 "*             Welcome to            *"
push 0
WB
storestrline 0 "*        EmojiVM 😀😁🤣🤔🤨😮       *"
push 0
WB
storestrline 0 "*       The Reverse Challenge       *"
push 0
WB
storestrline 0 "*                                   *"
push 0
WB
storestrline 0 "*************************************"
push 0
WB
storestrhex 0 "0a00"
push 0
WB
storestr 0 "Please input the secret: "
push 0
WB
# secret buffer: idx 1
pushnum 30
NEW
# enc buffer: idx 2
pushnum 30
NEW
# out buffer: idx 3  
pushnum 30
NEW
# check buffer: idx 4
pushnum 30
NEW
# store enc
storestrhex 2 "18051d1042094a24005b081740007230096c5640095b051a"
# store check
storestrhex 4 "8e63cd124b5815175122d904512c1915862cd14c842e2006"
# read input
push 1
RB

# strip newline, calculate len
# first new a byte array: idx 5
# can store 5 number
# [0]: len  [1]: secret string idx
push 5
NEW

CAL_LEN:
# load idx
push 1
push 5
LD
# load char from secret
push 1
LD
# eq null?
push 0
EQ
BRT CHECK_LEN
# load char from secret again
push 1
push 5
LD
push 1
LD
# eq \n ?
push 10
EQ
BRT STRIP
# if not \n and null, len++ and loop
# load len data
push 0
push 5
LD
# add 1
push 1
ADD
# store it back
push 0
push 5
ST
# idx++
push 1
push 5
LD
push 1
ADD
push 1
push 5
ST
# loop
BR CAL_LEN
STRIP:
# push null byte
push 0
push 1
push 5
LD
push 1
ST
BR CHECK_LEN


CHECK_LEN:
push 0
push 5
LD
pushnum 24
EQ
BRF FAIL

# clear idx
push 0
push 1
push 5
ST
CHECK_FORMAT:
# if idx+1 % 5 == 0, check if char == '-'
push 5
push 1
push 5
LD
push 1
ADD
MOD
push 0
eq
BRT CHECK_DASH
CHECK_FORMAT_NEXT:
# idx++
push 1
push 5
LD
push 1
ADD
push 1
push 5
ST
# idx < 24 ?
pushnum 24
push 1
push 5
LD
LT
BRT CHECK_FORMAT
BR OPERATE

CHECK_DASH:
pushnum 45
push 1
push 5
LD
push 1
LD
EQ
BRF FAIL
BR CHECK_FORMAT_NEXT

OPERATE:
# clear index
push 0
push 1
push 5
ST
OPERATE_LOOP:
# check value if idx % 4
push 4
push 1
push 5
LD
MOD
# store the value
push 2
push 5
ST
push 2
push 5
LD
push 0
EQ
BRT OP0
push 2
push 5
LD
push 1
EQ
BRT OP1
push 2
push 5
LD
push 2
EQ
BRT OP2
push 2
push 5
LD
push 3
EQ
BRT OP3
OPERATE_NEXT:
push 1
push 5
LD
push 1
ADD
push 1
push 5
ST
pushnum 24
push 1
push 5
LD
LT
BRT OPERATE_LOOP
BR VERIFY

OP0:
push 1
push 5
LD
push 1
LD
pushnum 30
ADD
push 1
push 5
LD
push 3
ST
BR OPERATE_NEXT

OP1:
push 8
push 1
push 5
LD
push 1
LD
SUB
push 7
XOR
push 1
push 5
LD
push 3
ST
BR OPERATE_NEXT

OP2:
push 4
push 1
push 5
LD
push 1
LD
pushnum 44
ADD
pushnum 68
XOR
SUB
push 1
push 5
LD
push 3
ST
BR OPERATE_NEXT

OP3:
push 1
push 5
LD
push 1
LD
pushnum 101
XOR
pushnum 172
pushnum 20
AND
XOR
push 1
push 5
LD
push 3
ST
BR OPERATE_NEXT


VERIFY:
# clear idx
push 0
push 1
push 5
ST
# clear data for cnt
push 0
push 2
push 5
ST
VERIFY_LOOP:
# out_buf[idx]
push 1
push 5
LD
push 3
LD
# check_buf[idx]
push 1
push 5
LD
push 4
LD
# if check_buf[idx] == out_buf[idx]
EQ
BRT CNT_PLUS
# cnt--
pushnum -1
push 2
push 5
LD
ADD
push 2
push 5
ST
VERIFY_NEXT:
# idx++
push 1
push 5
LD
push 1
ADD
push 1
push 5
ST
# if idx < 24
pushnum 24
push 1
push 5
LD
LT
BRT VERIFY_LOOP
BR CHECK_ANSWER

CNT_PLUS:
# cnt++
push 1
push 2
push 5
LD
ADD
push 2
push 5
ST
BR VERIFY_NEXT

CHECK_ANSWER:
push 2
push 5
LD
pushnum 24
EQ
BRF FAIL

# print flag
# clear idx
push 0
push 1
push 5
ST
DEC_LOOP:
# load secret[idx]
push 1
push 5
LD
push 1
LD
# load enc[idx]
push 1
push 5
LD
push 2
LD
# enc[idx] = enc[idx] ^ secret[idx]
XOR
push 1
push 5
LD
push 2
ST
# idx++
push 1
push 5
LD
push 1
ADD
push 1
push 5
ST
# if idx < 24
pushnum 24
push 1
push 5
LD
LT
BRT DEC_LOOP
BR SUCCESS

FAIL:
storestrline 0 "😭" 
push 0
WB
BR END

SUCCESS:
storestrline 0 "😍"
push 0
WB
push 2
WB
storestrline 0 ""
push 0
WB

END:
hlt
