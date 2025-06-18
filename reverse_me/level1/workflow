## scanf call
format stored in [esp] = 0x56557029 ("%s")
buffer stored in [esp+0x4] = 0xffffcf3c (random values)
```
   0x00001220 <+96>:	mov    DWORD PTR [esp],ecx
   0x00001223 <+99>:	mov    DWORD PTR [esp+0x4],eax
   0x00001227 <+103>:	call   0x1070 <__isoc99_scanf@plt>
```

## strcmp call
s1 and s2 are loaded on the program stack, using esp.
s1 [eax] = 0xffffcf3c (-> STRING PUT IN STDIN)
s2 [eax+0x4] = 0xffffcf2e (-> "__stack_check")
```
   0x00001235 <+117>:	mov    eax,esp
   0x00001237 <+119>:	mov    DWORD PTR [eax+0x4],edx
   0x0000123a <+122>:	mov    DWORD PTR [eax],ecx
   0x0000123c <+124>:	call   0x1040 <strcmp@plt>
```

## 0xffffcf2e definition
address+1 is put in ebx then add 0x2e31 : ebx = address+1 + 0x2e31.
0x2e31 never change and is position-independent, it's the offset to go back in a previous section
```
   address <+10>:	call   address+1 <main+15>
   address+1 <+15>:	pop    ebx
   address+2 <+16>:	add    ebx,0x2e31
```

from end to beginning:
(main+119) before strcmp call, 0xffffcf2e is loaded from edx
(main+114) edx loaded from ebp-0x7a
(main+38) ebp-0x7a loaded from eax
(main+32) eax loaded from ebx-0x1ff8

we saw previously that ebx is defined from address + offset(here 0x2e31).
then eax = address + 0x2e31 - 0x1ff8 = address + e39

during a gdb run, call instruction address argument was defined:
eax = 0x56557008 = 8 bytes after .rodata beginning
.rodata stores the read-only datas, the const ones (here it's "__stack_check")

```
(gdb) x/s 0x56557008
0x56557008:	"__stack_check"
```

## the size of the input buffer ?
buffer address: 0xffffcf3c
(main+99) 0xffffcf3c loaded from eax
(main+87) eax loaded from ebp-0x6c

ebp is a base pointer
the diff between ebp and esp defines the local variables available space.
ebp - esp = 0x84 = 132 bytes available

after dichotomous research, to find the input buffer size between 132 and 0,
I found out a segfault when the input is >= 112 bytes.
Input buffer has a size of ~112 including the \0 at the end.

## segfault doesn't appear at the same size in my source.c prgm copy ?
it is basically because the compiler doesnt manage the stack exactly the same way that the original compiler of the binary did.
it explains why i can write more or less than the original program in other local variables without triggering a segfault.
