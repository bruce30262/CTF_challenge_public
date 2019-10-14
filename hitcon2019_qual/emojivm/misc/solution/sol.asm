# tool/assembler.py sol.asm sol.evm
push 10
new
push 5
new
push 5
new
push 5
new
storestr 1 " * "
storestr 2 " = "
storestrline 3 ""

# for x = 1
push 1
push 0
push 0
ST
X_LOOP:
# if x < 10 ?
push 10
push 0
push 0
LD
LT
BRF END
# for y = 1
push 1
push 1
push 0
ST
Y_LOOP:
# if y == 10, goto x_next
push 10
push 1
push 0
LD
EQ
BRT X_NEXT
# cal x*y
push 0
push 0
LD
push 1
push 0
LD
mul
# store x*y
push 2
push 0
ST
# start print
push 0
push 0
LD
PN
push 1
WB
push 1
push 0
LD
PN
push 2
WB
push 2
push 0
LD
PN
push 3
WB
# y++
push 1
push 0
LD
push 1
ADD
push 1
push 0
ST
BR Y_LOOP

X_NEXT:
# x++
push 0
push 0
LD
push 1
ADD
push 0
push 0
ST
BR X_LOOP

END:
hlt

