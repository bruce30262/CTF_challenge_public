# Core Dumb  
* Category : reverse  
* Solved : 36  
> Damn it my flag checker is so buggy it destroyed the program itself 😱  
> All I left is a core dump file :(  
> Could you help me recover the flag ? Q_Q
> 
> Hint: sha256(flag) == 333fbc11481fca3501fff9f69f8f9c7d95f143272d451a3aea8c0b898379d88d  


This challenge was inspired by those [flare-on](http://flare-on.com/) challenges I've solved during the past 2 years :)  
Most of the idea were taken from [level 6 of flare-on 5](https://bruce30262.github.io/flare-on-challenge-2018-write-up/#level-6) and [level 12 of flare-on 6](https://bruce30262.github.io/flare-on-challenge-2019-write-up/#level-12).  
  
The purpose of this challenge is to let challengers analyze 5 encrypted flag-checking functions and try recovering the flag.  
You can check the source code of the flag checker in the src folder.  


### The code
Basically it has 6 functions. 5 of them will check the part of the flag, and the other one is for "testing purpose".  
All 6 functions will be encrypted with simple XOR operation. The encrypted code and their XOR keys are stored inside a global buffer, which shouldn't be difficult for you to discover. Once you find the key & the encrypted data you can just write a decryptor and get those function code.
  
The 6 functions are:  
1. `check1`: simple XOR/SUB operation.  
2. `check2`: customized XTEA. The `delta` was changed to `0x1337dead`.  
3. `check3`: customized base64 encoding. The base64 table is a randomized string. You'll have to implement the base64 decoding algorithm with the customized table.  
4. `check4`: customized RC4. This one is easy though. You can even use flare-emu or unicorn to run the function against the encrypted value then you'll get the plain text.  
5. `check5`: CRC32. This function only checks 4 bytes data, so you can just brute-force the last 4 bytes of the flag.  
> However I heard someone just use sha256 to brute-force the last 4 bytes data. Maybe I shouldn't provide the hash of the flag :/ ( The reason why I provide the hash is because there are 2 solutions for CRC32. However the other one is not printable, this should be enough for you guys to figure out the correct flag )  
6. `test()`: for "testing purpose", the idea is to "test so we can make sure that all the function has been decrypted successfully"  

## The core dump  
The idea of using core dump file as a challenge was inspired by this year's flare-on 6 challenge ( level 12 ). With this the challenger cannot execute/debug the program, and is required to analyze the binary with static analysis.


Here I just changed the decrypt key of `test()` to `0x00000000` so later when the program ran into `test()` it'll crash the program.  

At first I tried to let the kernel generate the core dump file for me. However for some unknown reason the core dump file didn't include the whole memory map.  
> I've set ulimit to unlimited, still don't know why it's not completed  

In the end I had to use gdb to execute the program and use the `generate-core-file` command to get the core dump file.  

## Misc  
For some reason IDA failed to decompile some functions in this one. Ghidra, on the other hand, decompiled all the functions successfully 😮  

## Epilogue  
Spent about 2 days creating this challenge, hope you all have fun while solving it 🙂



