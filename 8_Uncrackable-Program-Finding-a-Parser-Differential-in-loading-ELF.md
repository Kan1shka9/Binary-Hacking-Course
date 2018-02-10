#### 8. Uncrackable Program? Finding a Parser Differential in loading ELF

``fuzz.py``

```python
import random
import os

os.system("cp license_2 license_2_fuzz")

def flip_byte(in_bytes):
	i = random.randint(0,len(in_bytes))
	c = chr(random.randint(0,0xFF))
	return in_bytes[:i]+c+in_bytes[i+1:]

def copy_binary():
	with open("license_2", "rb") as orig_f, open("license_2_fuzz", "wb") as new_f:
		new_f.write(flip_byte(orig_f.read()))

def compare(fn1, fn2):
	with open(fn1) as f1, open(fn2) as f2:
		return f1.read()==f2.read()

def check_output():
	os.system("(./license_2_fuzz ; ./license_2_fuzz AAAA-Z10N-42-OK) > fuzz_output")
	return compare("orig_output", "fuzz_output")


def check_gdb():
	os.system("echo disassemble main | gdb license_2_fuzz > fuzz_gdb")
	return compare("orig_gdb", "fuzz_gdb")

def check_radare():
	os.system('echo -e "aaa\ns sym.main\npdf" | radare2 license_2_fuzz > fuzz_radare')
	return compare("orig_radare", "fuzz_radare")

while True:
	copy_binary()
	if check_output() and not check_gdb() and not check_radare():
		print "FOUND POSSIBLE FAIL\n\n\n"
		os.system("tail fuzz_gdb")
		os.system("tail fuzz_radare")
		raw_input()
```

```sh
l64@l64-virtual-machine:~$ python fuzz.py
Traceback (most recent call last):
  File "fuzz.py", line 34, in <module>
    if check_output() and not check_gdb() and not check_radare():
  File "fuzz.py", line 21, in check_output
    return compare("orig_output", "fuzz_output")
  File "fuzz.py", line 16, in compare
    with open(fn1) as f1, open(fn2) as f2:
IOError: [Errno 2] No such file or directory: 'orig_output'
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ (./license_2_fuzz; ./license_2_fuzz AAAA-Z10N-42-OK) > orig_output
```

```sh
l64@l64-virtual-machine:~$ cat orig_output
Usage: <key>
Checking License: AAAA-Z10N-42-OK
Access Granted!
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ echo disassemble main | gdb license_2_fuzz > orig_gdb
```

```sh
l64@l64-virtual-machine:~$ cat orig_gdb
GNU gdb (Ubuntu 8.0.1-0ubuntu1) 8.0.1
Copyright (C) 2017 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from license_2_fuzz...(no debugging symbols found)...done.
(gdb) Dump of assembler code for function main:
   0x00000000004005bd <+0>:	push   %rbp
   0x00000000004005be <+1>:	mov    %rsp,%rbp
   0x00000000004005c1 <+4>:	push   %rbx
   0x00000000004005c2 <+5>:	sub    $0x28,%rsp
   0x00000000004005c6 <+9>:	mov    %edi,-0x24(%rbp)
   0x00000000004005c9 <+12>:	mov    %rsi,-0x30(%rbp)
   0x00000000004005cd <+16>:	cmpl   $0x2,-0x24(%rbp)
   0x00000000004005d1 <+20>:	jne    0x400663 <main+166>
   0x00000000004005d7 <+26>:	mov    -0x30(%rbp),%rax
   0x00000000004005db <+30>:	add    $0x8,%rax
   0x00000000004005df <+34>:	mov    (%rax),%rax
   0x00000000004005e2 <+37>:	mov    %rax,%rsi
   0x00000000004005e5 <+40>:	mov    $0x400704,%edi
   0x00000000004005ea <+45>:	mov    $0x0,%eax
   0x00000000004005ef <+50>:	callq  0x4004a0 <printf@plt>
   0x00000000004005f4 <+55>:	movl   $0x0,-0x18(%rbp)
   0x00000000004005fb <+62>:	movl   $0x0,-0x14(%rbp)
   0x0000000000400602 <+69>:	jmp    0x400624 <main+103>
   0x0000000000400604 <+71>:	mov    -0x30(%rbp),%rax
   0x0000000000400608 <+75>:	add    $0x8,%rax
   0x000000000040060c <+79>:	mov    (%rax),%rdx
   0x000000000040060f <+82>:	mov    -0x14(%rbp),%eax
   0x0000000000400612 <+85>:	cltq
   0x0000000000400614 <+87>:	add    %rdx,%rax
   0x0000000000400617 <+90>:	movzbl (%rax),%eax
   0x000000000040061a <+93>:	movsbl %al,%eax
   0x000000000040061d <+96>:	add    %eax,-0x18(%rbp)
   0x0000000000400620 <+99>:	addl   $0x1,-0x14(%rbp)
   0x0000000000400624 <+103>:	mov    -0x14(%rbp),%eax
   0x0000000000400627 <+106>:	movslq %eax,%rbx
   0x000000000040062a <+109>:	mov    -0x30(%rbp),%rax
   0x000000000040062e <+113>:	add    $0x8,%rax
   0x0000000000400632 <+117>:	mov    (%rax),%rax
   0x0000000000400635 <+120>:	mov    %rax,%rdi
   0x0000000000400638 <+123>:	callq  0x400490 <strlen@plt>
   0x000000000040063d <+128>:	cmp    %rax,%rbx
   0x0000000000400640 <+131>:	jb     0x400604 <main+71>
   0x0000000000400642 <+133>:	cmpl   $0x394,-0x18(%rbp)
   0x0000000000400649 <+140>:	jne    0x400657 <main+154>
   0x000000000040064b <+142>:	mov    $0x40071a,%edi
   0x0000000000400650 <+147>:	callq  0x400480 <puts@plt>
   0x0000000000400655 <+152>:	jmp    0x40066d <main+176>
   0x0000000000400657 <+154>:	mov    $0x40072a,%edi
   0x000000000040065c <+159>:	callq  0x400480 <puts@plt>
   0x0000000000400661 <+164>:	jmp    0x40066d <main+176>
   0x0000000000400663 <+166>:	mov    $0x400731,%edi
   0x0000000000400668 <+171>:	callq  0x400480 <puts@plt>
   0x000000000040066d <+176>:	mov    $0x0,%eax
   0x0000000000400672 <+181>:	add    $0x28,%rsp
   0x0000000000400676 <+185>:	pop    %rbx
   0x0000000000400677 <+186>:	pop    %rbp
   0x0000000000400678 <+187>:	retq
End of assembler dump.
(gdb) quit
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ echo -e "aaa\ns main\npdf" | radare2 license_2_fuzz > orig_radare
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ python fuzz.py
BFD: /home/l64/license_2_fuzz: invalid string offset 8978676 >= 264 for section `.shstrtab'
BFD: /home/l64/license_2_fuzz: invalid string offset 8978676 >= 264 for section `.shstrtab'
"/home/l64/license_2_fuzz": not in executable format: Bad value
No symbol table is loaded.  Use the "file" command.
Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
FOUND POSSIBLE FAIL



and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
(gdb) (gdb) quit
 -- Beer in mind.
Vim: Error reading input, exiting...
Vim: preserving files...
Vim: Finished.
[0x004004d0]>
"/home/l64/license_2_fuzz": not in executable format: File format not recognized
No symbol table is loaded.  Use the "file" command.
Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
FOUND POSSIBLE FAIL



and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
(gdb) (gdb) quit
 -- Can you stand on your head?
Vim: Error reading input, exiting...
Vim: preserving files...
Vim: Finished.
[0x004004d0]>
Segmentation fault (core dumped)
Segmentation fault (core dumped)
Segmentation fault (core dumped)
Segmentation fault (core dumped)
Segmentation fault (core dumped)
Segmentation fault (core dumped)
Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
FOUND POSSIBLE FAIL



   0x0000000000400617 <+164>:	movzbl (%rax),%eax
   0x000000000040061a <+167>:	movsbl %al,%eax
   0x000000000040061d <+170>:	add    %eax,-0x18(%rbp)
   0x0000000000400620 <+173>:	addl   $0x1,-0x14(%rbp)
   0x0000000000400624 <+177>:	mov    -0x14(%rbp),%eax
   0x0000000000400627 <+180>:	movslq %eax,%rbx
   0x000000000040062a <+183>:	mov    -0x30(%rbp),%rax
   0x000000000040062e <+187>:	add    $0x8,%rax
End of assembler dump.
(gdb) quit
 -- That's embarrassing.
Vim: Error reading input, exiting...
Vim: preserving files...
Vim: Finished.
[0x004004d0]>
"/home/l64/license_2_fuzz": not in executable format: Bad value
No symbol table is loaded.  Use the "file" command.
Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal
FOUND POSSIBLE FAIL



and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
(gdb) (gdb) quit
 -- give | and > a try piping and redirection
Vim: Error reading input, exiting...
Vim: preserving files...
Vim: Finished.
[0x004004d0]> ^CTraceback (most recent call last):
  File "fuzz.py", line 38, in <module>
    raw_input()
KeyboardInterrupt
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ ./license_2_fuzz
Usage: <key>
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ ./license_2_fuzz WRONG-KEY
Checking License: WRONG-KEY
WRONG!
l64@l64-virtual-machine:~$
```

```sh
l64@l64-virtual-machine:~$ ./license_2_fuzz AAAA-Z10N-42-OK
Checking License: AAAA-Z10N-42-OK
Access Granted!
l64@l64-virtual-machine:~$
```

###### Parser Differential attack

- [BREAKING AND EVADING LINUX WITH A NEW NOVEL TECHNIQUE](https://www.sentinelone.com/blog/breaking-and-evading/)
- [Striking Back GDB and IDA debuggers through malformed ELF executables](http://blog.ioactive.com/2012/12/striking-back-gdb-and-ida-debuggers.html?m=1)
- [PoC||GTFO Journal # 0x00](http://openwall.info/wiki/_media/people/solar/pocorgtfo00.pdf)
	- [Index](http://openwall.info/wiki/people/solar/pocorgtfo)