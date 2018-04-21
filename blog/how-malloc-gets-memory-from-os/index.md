# How malloc gets memory from the OS
*Apr 22, 2018*

In the old days of 8086, 16-bit programs accessed physical memory directly.
This would be valid code and would work:

```
int main()
{
    int *p = (int *)0x02ad;
    return *p;
}
```

x86 processors still boot into 16-bit real mode where this is fine, but the
OS switches the processor into protected mode which enables virtual memory.
Once virtual memory is enabled, each process has its own virtual memory
that the OS has to map (to physical memory, files on the hard drive, device registers, etc.).
If the program tries to access unmapped memory, a segfault happens.

When Linux starts a process and loads the executable to memory, the layout of
the virtual address space looks something like this:

```
---------------
|             |
|    stack    |
|             |
--------------- 0x7ffc725866b4
|             |
|             |
|             |
|   unmapped  |
|    space    |
|             |
|             |
|             |
--------------- 0x000001773000
|             |
| data (bss)  |
|             |
---------------
|             |
|    data     |
|             |
---------------
|             |
|    text     |
|             |
---------------
```

The `text` segment contains the binary code of the executable, the `data` segment
has initialized static variables, the `bss` segment has uninitialized static variables
(zeroed out before main() function is called), and the `stack` segment contains the stack
(There's also space for the environment variables, and the OS kernel space is also mapped
for performance reasons, but I've skipped these in the diagram.) The adresses of 
the these segments is randomized when the executable is loaded as a security measure (ASLR).

When `malloc()` is called, it tries to allocate memory from previously freed memory that
is still mapped to the process. But if there is insufficient free memory, `malloc()` must
make one of these system calls to request the OS to map additional memory:

- The `brk` / `sbrk` system calls enlarge the data segment. In the diagram above, calling `sbrk(8)`
would move the end of the data segment from `0x1773000` to `0x1773008`. If the process wants
to free the memory and return it to the OS, the data segment can be shrunk with the same syscalls.

- The `mmap` syscall can map pages anywhere in the virtual address space (the equivalent syscall
in Windows is `VirtualAlloc`).

The `malloc` implementation in glibc uses `sbrk` when it needs small amounts of memory (~32K) and `mmap`
when it needs large amounts of memory. The reason `mmap` is preferred for large objects is to prevent
losing too much memory to fragmentation in the data segment; if a small object is allocated with `sbrk`
after a large object and then, if the large object is freed, that memory cannot be freed
until the small object is freed as well.

