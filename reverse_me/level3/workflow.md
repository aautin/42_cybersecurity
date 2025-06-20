# Info files
```
	Entry point: 0x10d0
	0x0000000000000318 - 0x0000000000000334 is .interp
	0x0000000000000338 - 0x0000000000000358 is .note.gnu.property
	0x0000000000000358 - 0x000000000000037c is .note.gnu.build-id
	0x000000000000037c - 0x000000000000039c is .note.ABI-tag
	0x00000000000003a0 - 0x00000000000003c8 is .gnu.hash
	0x00000000000003c8 - 0x0000000000000560 is .dynsym
	0x0000000000000560 - 0x000000000000063e is .dynstr
	0x000000000000063e - 0x0000000000000660 is .gnu.version
	0x0000000000000660 - 0x00000000000006a0 is .gnu.version_r
	0x00000000000006a0 - 0x0000000000000778 is .rela.dyn
	0x0000000000000778 - 0x0000000000000850 is .rela.plt
	0x0000000000001000 - 0x000000000000101b is .init
	0x0000000000001020 - 0x00000000000010c0 is .plt
	0x00000000000010c0 - 0x00000000000010c8 is .plt.got
	0x00000000000010d0 - 0x000000000000157f is .text
	0x0000000000001580 - 0x000000000000158d is .fini
	0x0000000000002000 - 0x000000000000205b is .rodata
	0x000000000000205c - 0x00000000000020e0 is .eh_frame_hdr
	0x00000000000020e0 - 0x00000000000022d0 is .eh_frame
	0x0000000000003de0 - 0x0000000000003de8 is .init_array
	0x0000000000003de8 - 0x0000000000003df0 is .fini_array
	0x0000000000003df0 - 0x0000000000003fd0 is .dynamic
	0x0000000000003fd0 - 0x0000000000004000 is .got
	0x0000000000004000 - 0x0000000000004060 is .got.plt
	0x0000000000004060 - 0x0000000000004070 is .data
	0x0000000000004070 - 0x0000000000004078 is .bss
```

# Utils functions analysis
## "___syscall_malloc"
put "Nope." (stored in .rodata) then exit(1)
```
   0x00000000000012e0 <+0>:	push   rbp
   0x00000000000012e1 <+1>:	mov    rbp,rsp
   0x00000000000012e4 <+4>:	lea    rdi,[rip+0xd48]        # 0x2033
   0x00000000000012eb <+11>:	call   0x1030 <puts@plt>
   0x00000000000012f0 <+16>:	mov    edi,0x1
   0x00000000000012f5 <+21>:	call   0x10b0 <exit@plt>
```

## "____syscall_malloc"
put "Good job." (stored in .rodata)
```
   0x0000000000001300 <+0>:	push   rbp
   0x0000000000001301 <+1>:	mov    rbp,rsp
   0x0000000000001304 <+4>:	lea    rdi,[rip+0xd2e]        # 0x2039
   0x000000000000130b <+11>:	call   0x1030 <puts@plt>
   0x0000000000001310 <+16>:	pop    rbp
   0x0000000000001311 <+17>:	ret    
```

## "not", "that", "easy"
print the name of the label plus a "." mark from .rodata

## "it", "try", "nice", "but", "this"
print the name of the label from .rodata

## "wt"
print "********" from .rodata

# "main' algorithm analysis
## receive input from stdin, "___syscall_malloc" if nothing's put
```
  0x0000000000001320 <+0>:	push   rbp
   0x0000000000001321 <+1>:	mov    rbp,rsp
   0x0000000000001324 <+4>:	sub    rsp,0x60
   0x0000000000001328 <+8>:	mov    DWORD PTR [rbp-0x4],0x0
   0x000000000000132f <+15>:	lea    rdi,[rip+0xd0d]        # 0x2043
   0x0000000000001336 <+22>:	mov    al,0x0
   0x0000000000001338 <+24>:	call   0x1050 <printf@plt>
   0x000000000000133d <+29>:	lea    rsi,[rbp-0x40]
   0x0000000000001341 <+33>:	lea    rdi,[rip+0xd0e]        # 0x2056
   0x0000000000001348 <+40>:	mov    al,0x0
   0x000000000000134a <+42>:	call   0x10a0 <__isoc99_scanf@plt>
   0x000000000000134f <+47>:	mov    DWORD PTR [rbp-0x8],eax
   0x0000000000001352 <+50>:	mov    eax,0x1
   0x0000000000001357 <+55>:	cmp    eax,DWORD PTR [rbp-0x8]
   0x000000000000135a <+58>:	je     0x1365 <main+69>
   0x0000000000001360 <+64>:	call   0x12e0 <___syscall_malloc>
```

scanf() format is "%23s" in .rodata
```
   0x0000000000001341 <+33>:	lea    rdi,[rip+0xd0e]        # 0x2056
   0x0000000000001348 <+40>:	mov    al,0x0
   0x000000000000134a <+42>:	call   0x10a0 <__isoc99_scanf@plt>
```
```
   (gdb) x/s 0x2056
   0x2056: "%23s"
```
then: input is stored from rbp-0x40 to rbp-0x29

## "___syscall_malloc" if input[1] != '2' or input[0] != '4'
```
   0x0000000000001365 <+69>:	movsx  ecx,BYTE PTR [rbp-0x3f]
   0x0000000000001369 <+73>:	mov    eax,0x32
   0x000000000000136e <+78>:	cmp    eax,ecx
   0x0000000000001370 <+80>:	je     0x137b <main+91>
   0x0000000000001376 <+86>:	call   0x12e0 <___syscall_malloc>
   0x000000000000137b <+91>:	movsx  ecx,BYTE PTR [rbp-0x40]
   0x000000000000137f <+95>:	mov    eax,0x34
   0x0000000000001384 <+100>:	cmp    eax,ecx
   0x0000000000001386 <+102>:	je     0x1391 <main+113>
   0x000000000000138c <+108>:	call   0x12e0 <___syscall_malloc>
```
input stored at [rbp-0x40], 0x32 == '2' and 0x34 == '4'

## flush stdin
[0x3fe0] = stdin file descriptor
```
   0x0000000000001391 <+113>:	mov    rax,QWORD PTR [rip+0x2c48]    # 0x3fe0
   0x0000000000001398 <+120>:	mov    rdi,QWORD PTR [rax]
   0x000000000000139b <+123>:	call   0x1080 <fflush@plt>
```

## clear stack-buffer
ptr is at rbp-0x21, value is 0, size is 9bytes (probably 8bytes passwd then)
```
   0x00000000000013a0 <+128>:	lea    rdi,[rbp-0x21]
   0x00000000000013a4 <+132>:	xor    esi,esi
   0x00000000000013a6 <+134>:	mov    edx,0x9
   0x00000000000013ab <+139>:	call   0x1060 <memset@plt>
```

## how to end the execution with a "Good job."
```
   0x00000000000014a2 <+386>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000000014a5 <+389>:	test   eax,eax
   [...]
   0x000000000000150d <+493>:	je     0x1568 <main+584>
   0x0000000000001513 <+499>:	jmp    0x1572 <main+594>
   0x0000000000001518 <+504>:	call   0x12e0 <___syscall_malloc>
   0x000000000000151d <+509>:	jmp    0x1577 <main+599>
   0x0000000000001522 <+514>:	call   0x12e0 <___syscall_malloc>
   0x0000000000001527 <+519>:	jmp    0x1577 <main+599>
   0x000000000000152c <+524>:	call   0x12e0 <___syscall_malloc>
   0x0000000000001531 <+529>:	jmp    0x1577 <main+599>
   0x0000000000001536 <+534>:	call   0x12e0 <___syscall_malloc>
   0x000000000000153b <+539>:	jmp    0x1577 <main+599>
   0x0000000000001540 <+544>:	call   0x12e0 <___syscall_malloc>
   0x0000000000001545 <+549>:	jmp    0x1577 <main+599>
   0x000000000000154a <+554>:	call   0x12e0 <___syscall_malloc>
   0x000000000000154f <+559>:	jmp    0x1577 <main+599>
   0x0000000000001554 <+564>:	call   0x12e0 <___syscall_malloc>
   0x0000000000001559 <+569>:	jmp    0x1577 <main+599>
   0x000000000000155e <+574>:	call   0x1300 <____syscall_malloc>
   0x0000000000001563 <+579>:	jmp    0x1577 <main+599>
   0x0000000000001568 <+584>:	call   0x12e0 <___syscall_malloc>
   0x000000000000156d <+589>:	jmp    0x1577 <main+599>
   0x0000000000001572 <+594>:	call   0x12e0 <___syscall_malloc>
```
The only way is to je on <main+584> so that eax arrives to the 0 value

```
   0x00000000000014a5 <+389>:	test   eax,eax
   0x00000000000014a7 <+391>:	je     0x155e <main+574>
```
eax (DWORD PTR [rbp-0x54]) == 0: "Good job."

```
   0x00000000000014a2 <+386>:	mov    eax,DWORD PTR [rbp-0x54]
   [...]
   0x00000000000014ad <+397>:	jmp    0x14b2 <main+402>
   0x00000000000014b2 <+402>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000000014b5 <+405>:	sub    eax,0x1
   0x00000000000014b8 <+408>:	je     0x1518 <main+504>
   0x00000000000014be <+414>:	jmp    0x14c3 <main+419>
   0x00000000000014c3 <+419>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000000014c6 <+422>:	sub    eax,0x2
   0x00000000000014c9 <+425>:	je     0x1522 <main+514>
   0x00000000000014cf <+431>:	jmp    0x14d4 <main+436>
   0x00000000000014d4 <+436>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000000014d7 <+439>:	sub    eax,0x3
   0x00000000000014da <+442>:	je     0x1540 <main+544>
   0x00000000000014e0 <+448>:	jmp    0x14e5 <main+453>
   0x00000000000014e5 <+453>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000000014e8 <+456>:	sub    eax,0x4
   0x00000000000014eb <+459>:	je     0x154a <main+554>
   0x00000000000014f1 <+465>:	jmp    0x14f6 <main+470>
   0x00000000000014f6 <+470>:	mov    eax,DWORD PTR [rbp-0x54]
   0x00000000000014f9 <+473>:	sub    eax,0x5
   0x00000000000014fc <+476>:	je     0x1554 <main+564>
   0x0000000000001502 <+482>:	jmp    0x1507 <main+487>
   0x0000000000001507 <+487>:	mov    eax,DWORD PTR [rbp-0x54]
   0x000000000000150a <+490>:	sub    eax,0x73
   0x000000000000150d <+493>:	je     0x1568 <main+584>
```
Jump to "___syscall_malloc" ("Nope.") if DWORD PTR [rbp-0x54] is equal to:
1 or 2 or 3 or 4 or 5 or any other values

## where eax (so DWORD PTR [rbp-0x54]) is starting from
```
   0x0000000000001475 <+341>:	call   0x1070 <strcmp@plt>
   0x000000000000147a <+346>:	mov    DWORD PTR [rbp-0x10],eax
   0x000000000000147d <+349>:	mov    eax,DWORD PTR [rbp-0x10]
   0x0000000000001480 <+352>:	mov    DWORD PTR [rbp-0x54],eax
```
eax (so DWORD PTR [rbp-0x54]) is the strcmp result

```
   0x0000000000001483 <+355>:	sub    eax,0xfffffffe
   0x0000000000001486 <+358>:	je     0x1536 <main+534>
   0x000000000000148c <+364>:	jmp    0x1491 <main+369>
   0x0000000000001491 <+369>:	mov    eax,DWORD PTR [rbp-0x54]
   0x0000000000001494 <+372>:	sub    eax,0xffffffff
   0x0000000000001497 <+375>:	je     0x152c <main+524>
   0x000000000000149d <+381>:	jmp    0x14a2 <main+386>

```
then on eax is applied two substraction but those two are equivalent to:
eax += 2 (<=> sub    eax,0xfffffffe)
eax += 1 (<=> sub    eax,0xffffffff)
because : eax = eax - 0xffffffff <=> eax = eax + (2^32 - 0xffffffff)

then it's going to "Nope." if strcmp result is equal to 1 or 2 still.

## what are we even comparing ?
```
   0x000000000000146a <+330>:	lea    rsi,[rip+0xb93]        # 0x2004
   0x0000000000001471 <+337>:	lea    rdi,[rbp-0x21]
   0x0000000000001475 <+341>:	call   0x1070 <strcmp@plt>
```
0x2004:		********
rbp-0x21:	the stack-buffer which was clear by memset at <main+139>

## ==> the final input has to be equal to "********"
the only part which isn't analysed is from <main+144> to <main+325>


## how is treated the input after enter it?
here is a while loop until the stack-buffer isnt 8bytes sized
```
   0x00000000000013c7 <+167>:	lea    rdi,[rbp-0x21]
   0x00000000000013cb <+171>:	call   0x1040 <strlen@plt>
   0x00000000000013d0 <+176>:	mov    rcx,rax
   0x00000000000013d3 <+179>:	xor    eax,eax
   0x00000000000013d5 <+181>:	cmp    rcx,0x8
   0x00000000000013d9 <+185>:	mov    BYTE PTR [rbp-0x45],al
   0x00000000000013dc <+188>:	jae    0x1403 <main+227>
```

### the content of the loop stands in 3 parts:
#### 1: put the 3 first input char in rbp-0x44, 0x43, 0x42, 0x41 = 0;
```
   0x0000000000001403 <+227>:	mov    al,BYTE PTR [rbp-0x45]
   0x0000000000001406 <+230>:	test   al,0x1
   0x0000000000001408 <+232>:	jne    0x1413 <main+243>
   0x000000000000140e <+238>:	jmp    0x1461 <main+321>
   0x0000000000001413 <+243>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000001417 <+247>:	mov    al,BYTE PTR [rbp+rax*1-0x40]
   0x000000000000141b <+251>:	mov    BYTE PTR [rbp-0x44],al
   0x000000000000141e <+254>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000001422 <+258>:	mov    al,BYTE PTR [rbp+rax*1-0x3f]
   0x0000000000001426 <+262>:	mov    BYTE PTR [rbp-0x43],al
   0x0000000000001429 <+265>:	mov    rax,QWORD PTR [rbp-0x18]
   0x000000000000142d <+269>:	mov    al,BYTE PTR [rbp+rax*1-0x3e]
   0x0000000000001431 <+273>:	mov    BYTE PTR [rbp-0x42],al
```

#### 2: put this 3chars str in atoi, put return number at stack-buffer[[rbp-0xc]]
```
   0x0000000000001434 <+276>:	lea    rdi,[rbp-0x44]
   0x0000000000001438 <+280>:	call   0x1090 <atoi@plt>
   0x000000000000143d <+285>:	mov    cl,al
   0x000000000000143f <+287>:	movsxd rax,DWORD PTR [rbp-0xc]
   0x0000000000001443 <+291>:	mov    BYTE PTR [rbp+rax*1-0x21],cl
```

#### 3: increment by 3 the input ptr, increment by one [rbp-0xc]
```
   0x0000000000001447 <+295>:	mov    rax,QWORD PTR [rbp-0x18]
   0x000000000000144b <+299>:	add    rax,0x3
   0x000000000000144f <+303>:	mov    QWORD PTR [rbp-0x18],rax
   0x0000000000001453 <+307>:	mov    eax,DWORD PTR [rbp-0xc]
   0x0000000000001456 <+310>:	add    eax,0x1
   0x0000000000001459 <+313>:	mov    DWORD PTR [rbp-0xc],eax
   0x000000000000145c <+316>:	jmp    0x13c7 <main+167>
```

## how is treated the input after enter it?
the loop will be executed 7 times to append a '*' on the stack-buffer.
the buffer already had a '*' at the 0-index
```
   0x00000000000013b0 <+144>:	mov    BYTE PTR [rbp-0x21],0x2a
```
