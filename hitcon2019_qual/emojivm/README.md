# Intro  
The whole idea of the EmojiVM started with a crazy thought that popped into my mind from nowhere:  
> Can we write an exploit with emojis 🤔 ?  

At first it was "just an crazy idea" which I thought I'll never implement.  
  
Until one day I found [this repo](https://github.com/codyebberson/vm) while googling for VM learning. After I look at its source code I found it's a perfect target for me to implement the idea of the "emoji exploit" -- it's simple, easy to modify, and most importantly, it already has some bugs in it !  
  
So I started implementing my own emoji VM. During the development I also realized it's a great target for creating a reverse/misc CTF challenge. In the end I've developed 3 CTF challenges and use them for the HITCON CTF 2019 Quals -- `EmojiVM`, `EmojiiVM` and `EmojiiiVM`. You can check the challenge source code and solutions in those folders.

# EmojiVM 
* Category : reverse  
* Solved : 77  
> A simple VM that takes emojis as input! Try figure out the secret!  

The idea of the reverse challenge popped into my mind while I was defining the emoji code. I thought it will be interesting to reverse an "emoji program". So after I finished developing the VM, I wrote a simple python crackme and converted it into an `evm` file. You can check the source code in the `rev` folder.  

The crackme is pretty simple, once it read the user's input ( secret ), it'll:  
1. Check the secret's length  
2. Check the secret's format  
3. Do some XOR/SUB/ADD operations base on the character's position and compare the result with a memory buffer.  
4. If the result is correct, XOR the secret with another buffer and print out the result, which should be the flag.

77 teams solved this one, which is lot more than I expected 😮 I guess I underestimate the power of dynamic analysis XD ( pure static analysis will be painful on this one )

# EmojiiVM  
* Category : misc  
* Solved : 66  
> It's time to test your emoji programming skill !  
> Make sure to check out readme.txt before you enter the challenge :)  
>
> nc 3.115.122.69 30261  
>
> Notice:  
> Make sure you send exact N bytes after you input N as your file size.  
> Otherwise the server might close the connection before it print out the flag !

I had lot of fun while developing the asm version of the reverse challenge. After developing an assembler for the EmojiVM, I started to write some assembly for the reverse challenge. It took me about 3 hours to complete the whole stuff. This made me think that it might be challenging ( and fun ! ) to develop an emoji program:  
* You'll have to write an assembler  
* You'll have to write an emoji program with your customized assembly  

That's the moment I decided to create another challenge: write a 9x9 multiplication table with emoji ! The reason why I choose the 9x9 multiplication table is because the challenger must use some branch instructions to complete the task, and writing an emoji assembler with branch instruction is not that easy. You can check the readme in tool/ for more details.

Another challenge while developing this task is blocking the un-intended solution. For example, a challenger can just use a simple read/write combo to print out the whole table, which is way too easy to achieve, that's why I add a filter to block the read instruction. Also since there are vulnerabilities in the binary, I've added some seccomp filter to prevent challenger solving the task by pwning the service. 

One last thing is about the service connection. During the CTF a guy ( from Tea Deliverers I think ? ) PM me in the IRC saying that the server close the connection after printing out the "Here's the flag:" message. After some debugging, I found that it's because the server ( python program ) uses `sys.stdin.read(N)` to read the emoji file. It'll read exact N bytes and if the challenger send more than N bytes, it'll close the connection before it print out the whole message. Because of this I added a notice message in the challenge description, reminding challengers to beware of the data bytes they sent. Later I fixed the code by changing

```python
print("Good job ! Here's the flag:")
print(FLAG)
```  

into  

```python
print("Good job ! Here's the flag:\n{}".format(FLAG))

```

Don't know if the fix works though, at least there were no complaint after I added the notice message.  

In the end 66 teams solved this challenge. I hope you guys have fun developing tools & writing the emoji program while solving this one 🙂


# EmojiiiVM  
* Category : pwn
* Solved : 39  
> Have you ever wrote an "emoji exploit" ?  
> Well now it's your chance! Pwn the service and get the flag ;)  
> 
> nc 3.115.176.164 30262 

Time to talk about the challenge that starts the whole thing XD  

So fun fact: while developing the VM, I tried as hard as I could to NOT write a vulnerable VM. Once I found a vulnerability during the development, I patched it immediately. My plan was to develop the VM as secure as possible, and see if I could spot some vulnerabilities while solving the challenge myself. If it still contains vulnerabilities, examine the bug and see if it is exploitable.  

This turned out to be a great plan XD I didn't notice the stack underflow vulnerability until I started reviewing my code more carefully. At first the `gptr` array was behind the VM stack buffer so it is not exploitable. However because I want this to be a "friendly" challenge, I decided to move the `gptr` array and place it in front of the VM stack, so challenger can pwn the service more easily. Just modify the pointer in `gptr`, it should be easy to create an arbitrary read/write primitive, overwrite `free_hook` to `system` and get the shell.

> BTW I'm not sure how many vulnerabilities are in this VM actually 😅 I found like 4 or 5 while reviewing my code, all related to the boundary check. Glad I'm not a developer in real life (?)

39 teams solved this one. I was excepting more though, after all there's no complicated heap manipulation or need some weird trick in libc -- all you need to do is overwrite the pointer with some emojis 🙂


## Epilogue  
Hope you all enjoy solving these challenges ! Feedbacks are always  welcome ! See you guys next year 😄



