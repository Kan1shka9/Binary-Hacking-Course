#### 18. Global Offset Table (GOT) and Procedure Linkage Table (PLT)

`text.c`

```c
int main()
{
	printf("Hello World!\n");
	printf("This is LiveOverflow\n");
	exit(0);
	return 1;
}
```

```sh
m64@vm ~ $ gcc text.c -o text
text.c: In function ‘main’:
text.c:3:2: warning: implicit declaration of function ‘printf’ [-Wimplicit-function-declaration]
  printf("Hello World!\n");
  ^
text.c:3:2: warning: incompatible implicit declaration of built-in function ‘printf’
text.c:3:2: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
text.c:5:2: warning: implicit declaration of function ‘exit’ [-Wimplicit-function-declaration]
  exit(0);
  ^
text.c:5:2: warning: incompatible implicit declaration of built-in function ‘exit’
text.c:5:2: note: include ‘<stdlib.h>’ or provide a declaration of ‘exit’
m64@vm ~ $
```

```sh
m64@vm ~ $ ./text
Hello World!
This is LiveOverflow
m64@vm ~ $
```

```sh
m64@vm ~ $ ldd text
	linux-vdso.so.1 =>  (0x00007fff6c1f6000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1dd49a8000)
	/lib64/ld-linux-x86-64.so.2 (0x00005650c49ff000)
m64@vm ~ $ ldd text
	linux-vdso.so.1 =>  (0x00007ffe44b41000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fe4c36f3000)
	/lib64/ld-linux-x86-64.so.2 (0x000055c2a1662000)
m64@vm ~ $ ldd text
	linux-vdso.so.1 =>  (0x00007ffe18f89000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f004b82e000)
	/lib64/ld-linux-x86-64.so.2 (0x0000559ffe175000)
m64@vm ~ $
```

![](images/18/1.png)

![](images/18/2.png)

![](images/18/3.png)

![](images/18/4.png)

![](images/18/5.png)

![](images/18/6.png)

![](images/18/7.png)

![](images/18/8.png)

![](images/18/9.png)

![](images/18/10.png)

![](images/18/11.png)

![](images/18/12.png)

```sh
m64@vm ~ $ strace ./text
execve("./text", ["./text"], [/* 22 vars */]) = 0
brk(NULL)                               = 0x104c000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=105198, ...}) = 0
mmap(NULL, 105198, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f7755882000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\t\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1868984, ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f7755881000
mmap(NULL, 3971488, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f77552ad000
mprotect(0x7f775546d000, 2097152, PROT_NONE) = 0
mmap(0x7f775566d000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1c0000) = 0x7f775566d000
mmap(0x7f7755673000, 14752, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f7755673000
close(3)                                = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f7755880000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f775587f000
arch_prctl(ARCH_SET_FS, 0x7f7755880700) = 0
mprotect(0x7f775566d000, 16384, PROT_READ) = 0
mprotect(0x600000, 4096, PROT_READ)     = 0
mprotect(0x7f775589c000, 4096, PROT_READ) = 0
munmap(0x7f7755882000, 105198)          = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 0), ...}) = 0
brk(NULL)                               = 0x104c000
brk(0x106d000)                          = 0x106d000
write(1, "Hello World!\n", 13Hello World!
)          = 13
write(1, "This is LiveOverflow\n", 21This is LiveOverflow
)  = 21
exit_group(0)                           = ?
+++ exited with 0 +++
m64@vm ~ $
```

![](images/18/13.png)

```sh
m64@vm ~ $ man ld.so
```

![](images/18/14.png)

![](images/18/15.png)

![](images/18/16.png)

![](images/18/17.png)