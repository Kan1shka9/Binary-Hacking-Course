#### 27. Socket programming in python and Integer Overflow

```sh
m64@vm ~ $ strace nc -l 1234
execve("/bin/nc", ["nc", "-l", "1234"], [/* 22 vars */]) = 0
brk(NULL)                               = 0x13d9000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=106484, ...}) = 0
mmap(NULL, 106484, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f2c18211000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/x86_64-linux-gnu/libbsd.so.0", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0004\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=81040, ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f2c18210000
mmap(NULL, 2179952, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f2c17df1000
mprotect(0x7f2c17e04000, 2093056, PROT_NONE) = 0
mmap(0x7f2c18003000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x12000) = 0x7f2c18003000
mmap(0x7f2c18005000, 880, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f2c18005000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/x86_64-linux-gnu/libresolv.so.2", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P9\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=101200, ...}) = 0
mmap(NULL, 2206280, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f2c17bd6000
mprotect(0x7f2c17bed000, 2097152, PROT_NONE) = 0
mmap(0x7f2c17ded000, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x17000) = 0x7f2c17ded000
mmap(0x7f2c17def000, 6728, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f2c17def000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\t\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1868984, ...}) = 0
mmap(NULL, 3971488, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f2c1780c000
mprotect(0x7f2c179cc000, 2097152, PROT_NONE) = 0
mmap(0x7f2c17bcc000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1c0000) = 0x7f2c17bcc000
mmap(0x7f2c17bd2000, 14752, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f2c17bd2000
close(3)                                = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f2c1820f000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f2c1820e000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f2c1820d000
arch_prctl(ARCH_SET_FS, 0x7f2c1820e700) = 0
mprotect(0x7f2c17bcc000, 16384, PROT_READ) = 0
mprotect(0x7f2c17ded000, 4096, PROT_READ) = 0
mprotect(0x7f2c18003000, 4096, PROT_READ) = 0
mprotect(0x606000, 4096, PROT_READ)     = 0
mprotect(0x7f2c1822b000, 4096, PROT_READ) = 0
munmap(0x7f2c18211000, 106484)          = 0
brk(NULL)                               = 0x13d9000
brk(0x13fa000)                          = 0x13fa000
socket(PF_INET, SOCK_STREAM, IPPROTO_TCP) = 3
setsockopt(3, SOL_SOCKET, SO_REUSEADDR, [1], 4) = 0
bind(3, {sa_family=AF_INET, sin_port=htons(1234), sin_addr=inet_addr("0.0.0.0")}, 16) = 0
listen(3, 1)                            = 0
accept(3, {sa_family=AF_INET, sin_port=htons(51368), sin_addr=inet_addr("127.0.0.1")}, [16]) = 4
close(3)                                = 0
poll([{fd=4, events=POLLIN}, {fd=0, events=POLLIN}], 2, -1) = 1 ([{fd=4, revents=POLLIN}])
read(4, "Hello From Client\n", 2048)    = 18
write(1, "Hello From Client\n", 18Hello From Client
)     = 18
poll([{fd=4, events=POLLIN}, {fd=0, events=POLLIN}], 2, -1Hello From Server
) = 1 ([{fd=0, revents=POLLIN}])
read(0, "Hello From Server\n", 2048)    = 18
write(4, "Hello From Server\n", 18)     = 18
poll([{fd=4, events=POLLIN}, {fd=0, events=POLLIN}], 2, -1) = 1 ([{fd=4, revents=POLLIN}])
read(4, "", 2048)                       = 0
shutdown(4, SHUT_RD)                    = 0
close(4)                                = 0
close(3)                                = -1 EBADF (Bad file descriptor)
close(3)                                = -1 EBADF (Bad file descriptor)
exit_group(0)                           = ?
+++ exited with 0 +++
m64@vm ~ $
```

```sh
m64@vm ~ $ nc 127.0.0.1 1234
Hello From Client
Hello From Server
^C
m64@vm ~ $
```

###### Protostar Net1

- About
	- This level tests the ability to convert binary integers into ascii representation.
	- This level is at `/opt/protostar/bin/net1`

`net1.c`

```c
#include "../common/common.c"

#define NAME "net1"
#define UID 998
#define GID 998
#define PORT 2998

void run()
{
  char buf[12];
  char fub[12];
  char *q;

  unsigned int wanted;

  wanted = random();

  sprintf(fub, "%d", wanted);

  if(write(0, &wanted, sizeof(wanted)) != sizeof(wanted)) {
      errx(1, ":(\n");
  }

  if(fgets(buf, sizeof(buf)-1, stdin) == NULL) {
      errx(1, ":(\n");
  }

  q = strchr(buf, '\r'); if(q) *q = 0;
  q = strchr(buf, '\n'); if(q) *q = 0;

  if(strcmp(fub, buf) == 0) {
      printf("you correctly sent the data\n");
  } else {
      printf("you didn't send the data properly\n");
  }
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  /* Don't do this :> */
  srandom(time(NULL));

  run();
}
```

- Solution

```sh
root@protostar:/opt/protostar/bin# netstat -plant
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      1050/portmap
tcp        0      0 0.0.0.0:2993            0.0.0.0:*               LISTEN      1613/final2
tcp        0      0 0.0.0.0:2994            0.0.0.0:*               LISTEN      1611/final1
tcp        0      0 0.0.0.0:2995            0.0.0.0:*               LISTEN      1609/final0
tcp        0      0 0.0.0.0:2996            0.0.0.0:*               LISTEN      1605/net3
tcp        0      0 0.0.0.0:2997            0.0.0.0:*               LISTEN      1603/net2
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1745/sshd
tcp        0      0 0.0.0.0:2998            0.0.0.0:*               LISTEN      1601/net1
tcp        0      0 0.0.0.0:2999            0.0.0.0:*               LISTEN      1599/net0
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      1588/exim4
tcp        0      0 0.0.0.0:33565           0.0.0.0:*               LISTEN      1062/rpc.statd
tcp        0      0 192.168.150.13:22       192.168.150.3:49979     ESTABLISHED 1775/sshd: user [pr
tcp        0      0 192.168.150.13:22       192.168.150.3:50155     ESTABLISHED 1821/sshd: user [pr
tcp6       0      0 :::22                   :::*                    LISTEN      1745/sshd
tcp6       0      0 ::1:25                  :::*                    LISTEN      1588/exim4
root@protostar:/opt/protostar/bin#
```

- [`What is the difference between AF_INET and PF_INET constants?`](https://stackoverflow.com/questions/2549461/what-is-the-difference-between-af-inet-and-pf-inet-constants)
- [`socket - 3.6`](https://docs.python.org/3/library/socket.html)
- [`socket - 2.7`](https://docs.python.org/2/library/socket.html)

`net1.py`

```python
import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 2998
s.connect((HOST, PORT))
n = s.recv(4)
print n
print repr(n)
print n.encode('hex')
```

```sh
root@protostar:/tmp# python net1.py
���x
'\x8f\x84\xc4x'
8f84c478
root@protostar:/tmp# python net1.py
e�u&
'e\xa8u&'
65a87526
root@protostar:/tmp# python net1.py
H��S
'H\x89\xf9S'
4889f953
root@protostar:/tmp# python net1.py
dX�
'dX\xa0\x01'
6458a001
root@protostar:/tmp# python net1.py
dX�
'dX\xa0\x01'
6458a001
root@protostar:/tmp# python net1.py
R#-0
'R#-0'
52232d30
root@protostar:/tmp#
```

`net1.py`

```python
import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 2998
s.connect((HOST, PORT))
n = s.recv(4)
print n
print repr(n)
print n.encode('hex')
N = struct.unpack("I", n)[0]
print N
s.send(str(N))
print s.recv(1024)
```

```sh
root@protostar:/tmp# python net1.py
n
V
'n\r\x0bV'
6e0d0b56
1443564910
you correctly sent the data
root@protostar:/tmp#
```

###### Protostar Net2

- About
	- This code tests the ability to add up `4 unsigned 32-bit integers`. 
	- Hint: Keep in mind that it wraps.
	- This level is at `/opt/protostar/bin/net2`

`net2.c`

```c
#include "../common/common.c"

#define NAME "net2"
#define UID 997
#define GID 997
#define PORT 2997

void run()
{
  unsigned int quad[4];
  int i;
  unsigned int result, wanted;

  result = 0;
  for(i = 0; i < 4; i++) {
      quad[i] = random();
      result += quad[i];

      if(write(0, &(quad[i]), sizeof(result)) != sizeof(result)) {
          errx(1, ":(\n");
      }
  }

  if(read(0, &wanted, sizeof(result)) != sizeof(result)) {
      errx(1, ":<\n");
  }


  if(result == wanted) {
      printf("you added them correctly\n");
  } else {
      printf("sorry, try again. invalid\n");
  }
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  /* Don't do this :> */
  srandom(time(NULL));

  run();
}
```

- Solution

```sh
root@protostar:/opt/protostar/bin# netstat -plant
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      1050/portmap
tcp        0      0 0.0.0.0:2993            0.0.0.0:*               LISTEN      1613/final2
tcp        0      0 0.0.0.0:2994            0.0.0.0:*               LISTEN      1611/final1
tcp        0      0 0.0.0.0:2995            0.0.0.0:*               LISTEN      1609/final0
tcp        0      0 0.0.0.0:2996            0.0.0.0:*               LISTEN      1605/net3
tcp        0      0 0.0.0.0:2997            0.0.0.0:*               LISTEN      1603/net2
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1745/sshd
tcp        0      0 0.0.0.0:2998            0.0.0.0:*               LISTEN      1601/net1
tcp        0      0 0.0.0.0:2999            0.0.0.0:*               LISTEN      1599/net0
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      1588/exim4
tcp        0      0 0.0.0.0:33565           0.0.0.0:*               LISTEN      1062/rpc.statd
tcp        0      0 192.168.150.13:22       192.168.150.3:49979     ESTABLISHED 1775/sshd: user [pr
tcp        0      0 192.168.150.13:22       192.168.150.3:50155     ESTABLISHED 1821/sshd: user [pr
tcp6       0      0 :::22                   :::*                    LISTEN      1745/sshd
tcp6       0      0 ::1:25                  :::*                    LISTEN      1588/exim4
root@protostar:/opt/protostar/bin#
```

`net2.py`

```
import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 2997
s.connect((HOST, PORT))
n = s.recv(4)
n += s.recv(4)
n += s.recv(4)
n += s.recv(4)
print n
print repr(n)
print n.encode('hex')
N = struct.unpack("IIII", n)
print N
sN = sum(N)
print sN
s.send(struct.pack("I",sN & 0xffffffff))
print s.recv(1024)
```

```sh
root@protostar:/tmp# python net2.py
b\K�ƘU�%c6qx
'b\x01\\K\xf9\xc6\x98U\xce%c6qx\x1b\x02'
62015c4bf9c69855ce25633671781b02
(1264320866, 1436075769, 912467406, 35354737)
3648218778
you added them correctly
root@protostar:/tmp#
```