#### 15. Ret2libc with a Buffer Overflow because of restricted return pointer

`Stack6` looks at what happens when you have restrictions on the return address.

- This level can be done in a couple of ways, such as finding the duplicate of the payload (objdump -s) will help with this), or `ret2libc`, or even `return orientated programming`.
- It is strongly suggested you experiment with multiple ways of getting your code to execute here.
- This level is at `/opt/protostar/bin/stack6`

`stack6.c`

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xbf000000) == 0xbf000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

```sh
user@protostar:/opt/protostar/bin$ ./stack6
input path please: AAAAAAAAAAAAAAAAAA
got path AAAAAAAAAAAAAAAAAA
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack6 -q
Reading symbols from /opt/protostar/bin/stack6...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble getpath
Dump of assembler code for function getpath:
0x08048484 <getpath+0>:	push   ebp
0x08048485 <getpath+1>:	mov    ebp,esp
0x08048487 <getpath+3>:	sub    esp,0x68
0x0804848a <getpath+6>:	mov    eax,0x80485d0
0x0804848f <getpath+11>:	mov    DWORD PTR [esp],eax
0x08048492 <getpath+14>:	call   0x80483c0 <printf@plt>
0x08048497 <getpath+19>:	mov    eax,ds:0x8049720
0x0804849c <getpath+24>:	mov    DWORD PTR [esp],eax
0x0804849f <getpath+27>:	call   0x80483b0 <fflush@plt>
0x080484a4 <getpath+32>:	lea    eax,[ebp-0x4c]
0x080484a7 <getpath+35>:	mov    DWORD PTR [esp],eax
0x080484aa <getpath+38>:	call   0x8048380 <gets@plt>
0x080484af <getpath+43>:	mov    eax,DWORD PTR [ebp+0x4]
0x080484b2 <getpath+46>:	mov    DWORD PTR [ebp-0xc],eax
0x080484b5 <getpath+49>:	mov    eax,DWORD PTR [ebp-0xc]
0x080484b8 <getpath+52>:	and    eax,0xbf000000
0x080484bd <getpath+57>:	cmp    eax,0xbf000000
0x080484c2 <getpath+62>:	jne    0x80484e4 <getpath+96>
0x080484c4 <getpath+64>:	mov    eax,0x80485e4
0x080484c9 <getpath+69>:	mov    edx,DWORD PTR [ebp-0xc]
0x080484cc <getpath+72>:	mov    DWORD PTR [esp+0x4],edx
0x080484d0 <getpath+76>:	mov    DWORD PTR [esp],eax
0x080484d3 <getpath+79>:	call   0x80483c0 <printf@plt>
0x080484d8 <getpath+84>:	mov    DWORD PTR [esp],0x1
0x080484df <getpath+91>:	call   0x80483a0 <_exit@plt>
0x080484e4 <getpath+96>:	mov    eax,0x80485f0
0x080484e9 <getpath+101>:	lea    edx,[ebp-0x4c]
0x080484ec <getpath+104>:	mov    DWORD PTR [esp+0x4],edx
0x080484f0 <getpath+108>:	mov    DWORD PTR [esp],eax
0x080484f3 <getpath+111>:	call   0x80483c0 <printf@plt>
0x080484f8 <getpath+116>:	leave
0x080484f9 <getpath+117>:	ret
End of assembler dump.
(gdb) break *getpath
Breakpoint 1 at 0x8048484: file stack6/stack6.c, line 7.
(gdb) r
Starting program: /opt/protostar/bin/stack6

Breakpoint 1, getpath () at stack6/stack6.c:7
7	stack6/stack6.c: No such file or directory.
	in stack6/stack6.c
(gdb) info proc map
process 3975
cmdline = '/opt/protostar/bin/stack6'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack6'
Mapped address spaces:

	Start Addr   End Addr       Size     Offset objfile
	 0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack6
	 0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack6
	0xb7e96000 0xb7e97000     0x1000          0
	0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
	0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
	0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
	0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
	0xb7fd9000 0xb7fdc000     0x3000          0
	0xb7fe0000 0xb7fe2000     0x2000          0
	0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
	0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
	0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
	0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
	0xbffeb000 0xc0000000    0x15000          0           [stack]
(gdb) info registers
eax            0xbffff844	-1073743804
ecx            0xec4cc6c8	-330512696
edx            0x1	1
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff78c	0xbffff78c
ebp            0xbffff798	0xbffff798
esi            0x0	0
edi            0x0	0
eip            0x8048484	0x8048484 <getpath>
eflags         0x200286	[ PF SF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb)
```

