CC:=g++
CFLAGS:= -std=c++11
exe:=emojivm
obj:=main.o vm.o

SECCOMP ?= 0
ifeq ($(SECCOMP), 1)
	CFLAGS =-DSECCOMP
endif

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	CFLAGS =-DDEBUG
endif

all:$(obj)
	 $(CC) -o $(exe) $(obj)
%.o:%.cc
	 $(CC) $(CFLAGS) -c $< -o $@

.PHONY:clean
clean:
	rm -rf $(obj) $(exe)
