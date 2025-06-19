# Circuit from main+0 to main+422 \<ok\>

## 1. main+78 : scanf() == 1 ? go to step 2 : <or>
```
	0x0000131b <+75>:	cmp    eax,DWORD PTR [ebp-0xc]
	0x0000131e <+78>:	je     0x132c <main+92>
```

## 2. main+103 : input[1] == '0' ? go to step 3 : <or>
```
	0x000012fe <+46>:	lea    eax,[ebp-0x35]
	[...]
	0x0000130a <+58>:	mov    DWORD PTR [esp+0x4],eax
	0x0000130e <+62>:	call   0x10c0 <__isoc99_scanf@plt>
	[...]
	0x0000132c <+92>:	movsx  ecx,BYTE PTR [ebp-0x34]
	0x00001330 <+96>:	mov    eax,0x30
	0x00001335 <+101>:	cmp    eax,ecx
	0x00001337 <+103>:	je     0x1345 <main+117>
```

## 3. main+128 : input[0] == '0' ? go to step 4 : <or>
```
   0x00001345 <+117>:	movsx  ecx,BYTE PTR [ebp-0x35]
   0x00001349 <+121>:	mov    eax,0x30
   0x0000134e <+126>:	cmp    eax,ecx
   0x00001350 <+128>:	je     0x135e <main+142>
```

## clear [ebp-0x1d] stack-buffer, init it on buffer[0] = 'd'
```
   0x00001356 <+134>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001359 <+137>:	call   0x1220 \<no\>
   0x0000135e <+142>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001361 <+145>:	mov    eax,DWORD PTR [ebx-0xc]
   0x00001367 <+151>:	mov    eax,DWORD PTR [eax]
   0x00001369 <+153>:	mov    ecx,DWORD PTR [ebx-0xc]
   0x0000136f <+159>:	mov    DWORD PTR [esp],eax
   0x00001372 <+162>:	call   0x1070 <fflush@plt>
   0x00001377 <+167>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x0000137a <+170>:	lea    eax,[ebp-0x1d]
   0x0000137d <+173>:	xor    ecx,ecx
   0x0000137f <+175>:	mov    DWORD PTR [esp],eax
   0x00001382 <+178>:	mov    DWORD PTR [esp+0x4],0x0
   0x0000138a <+186>:	mov    DWORD PTR [esp+0x8],0x9
   0x00001392 <+194>:	call   0x10b0 <memset@plt>
   0x00001397 <+199>:	mov    BYTE PTR [ebp-0x1d],0x64
   0x0000139b <+203>:	mov    BYTE PTR [ebp-0x36],0x0
   0x0000139f <+207>:	mov    DWORD PTR [ebp-0x14],0x2
   0x000013a6 <+214>:	mov    DWORD PTR [ebp-0x10],0x1
```

## 4. main+246 : strlen(buffer) < 8 ? go to step 5 : go to \<ok\>
ebp-0x1d is memset on 9 zero bytes, then put a 'd' at 1st index
```
   0x0000137a <+170>:	lea    eax,[ebp-0x1d]
   [...]
   0x0000137f <+175>:	mov    DWORD PTR [esp],eax
   0x00001382 <+178>:	mov    DWORD PTR [esp+0x4],0x0
   0x0000138a <+186>:	mov    DWORD PTR [esp+0x8],0x9
   0x00001392 <+194>:	call   0x10b0 <memset@plt>
   [...]
   0x00001397 <+199>:	mov    BYTE PTR [ebp-0x1d],0x64 ;'d' == 0x64
```

compare the length string at ebp-0x1d with 8
```
   0x000013b0 <+224>:	lea    ecx,[ebp-0x1d]
   0x000013b3 <+227>:	mov    eax,esp
   0x000013b5 <+229>:	mov    DWORD PTR [eax],ecx
   0x000013b7 <+231>:	call   0x10a0 <strlen@plt>
   0x000013bc <+236>:	mov    ecx,eax
   0x000013be <+238>:	xor    eax,eax
   0x000013c0 <+240>:	cmp    ecx,0x8
   0x000013c6 <+246>:	jae    0x13ee <main+286>
```

## 5. main+297 : 2 < strlen(input)
ecx = eax = strlen(input)
```
   0x000013d5 <+261>:	lea    ecx,[ebp-0x35]
   [...]
   0x000013da <+266>:	mov    DWORD PTR [eax],ecx
   0x000013dc <+268>:	call   0x10a0 <strlen@plt>
   0x000013e1 <+273>:	mov    ecx,eax
```

eax = DWORD PTR [ebp-0x48] = DWORD PTR [ebp-0x14] = 0x2
```
   0x0000139f <+207>:	mov    DWORD PTR [ebp-0x14],0x2
   0x000013cf <+255>:	mov    eax,DWORD PTR [ebp-0x14]
   0x000013d2 <+258>:	mov    DWORD PTR [ebp-0x48],eax
   [...]
   0x000013e3 <+275>:	mov    eax,DWORD PTR [ebp-0x48]
```

al = eax < ecx
```
   0x000013e1 <+273>:	mov    ecx,eax
   0x000013e3 <+275>:	mov    eax,DWORD PTR [ebp-0x48]
   0x000013e6 <+278>:	cmp    eax,ecx
   0x000013e8 <+280>:	setb   al
```

(al == 1) ? go to step 7 (main+378) : go to step 6 (main+302)
```
   0x000013f1 <+289>:	test   al,0x1
   0x000013f3 <+291>:	jne    0x13fe <main+302>
   0x000013f9 <+297>:	jmp    0x144a <main+378>
```

## 6. main+432 : is stack-buffer == readonly-string ? \<ok\> : \<no\>
ecx = [ebp-0x1d] = "d"
```
   0x0000137a <+170>:	lea    eax,[ebp-0x1d]
   [...]
   0x0000137f <+175>:	mov    DWORD PTR [esp],eax
   0x00001382 <+178>:	mov    DWORD PTR [esp+0x4],0x0
   0x0000138a <+186>:	mov    DWORD PTR [esp+0x8],0x9
   0x00001392 <+194>:	call   0x10b0 <memset@plt>
   [...]
   0x00001397 <+199>:	mov    BYTE PTR [ebp-0x1d],0x64
   [...]
   0x00001455 <+389>:	lea    ecx,[ebp-0x1d]
```

edx = [ebx-0x42cd] = 0x12dc + 0x5d24 - 0x42cd = 0x2d33 = "delabere"
```
   0x000012d7 <+7>:	call   0x12dc <main+12>
   0x000012dc <+12>:	pop    ebx
   0x000012dd <+13>:	add    ebx,0x5d24
   [...]
   0x0000144a <+378>:	mov    ebx,DWORD PTR [ebp-0x40]
   [...]
   0x00001455 <+389>:	lea    ecx,[ebp-0x1d]
   0x00001458 <+392>:	lea    edx,[ebx-0x42cd]
```

in gdb, sections info, we see 0x2d33 belongs to .rodata
```
(gdb)    info files
   [...]
	0x000010f0 - 0x000015eb is .text
	0x000015ec - 0x00001604 is .fini
	0x00002000 - 0x00005494 is .rodata
	0x00005494 - 0x00005500 is .eh_frame_hdr
	0x00005500 - 0x0000568c is .eh_frame
   [...]
```

strcmp("delabere", "d")
```
   0x0000145e <+398>:	mov    eax,esp
   0x00001460 <+400>:	mov    DWORD PTR [eax+0x4],edx
   0x00001463 <+403>:	mov    DWORD PTR [eax],ecx
   0x00001465 <+405>:	call   0x1040 <strcmp@plt>
```

"delabere" is readonly.
the only way to arrive here, don't jump and go to \<ok\> is to modify
the string from [ebp-0x1d] (in step 7)
```
   0x0000146a <+410>:	cmp    eax,0x0
   0x0000146d <+413>:	jne    0x1480 <main+432>
```

## 7. main+? : a loop to go modify [ebp-0x1d] and go back to step 5
in this section, the 3 first bytes of the input are put in atoi, turned
into a number which is appened to the stack-buffer.
the input ptr is incremented by 3, then go back to step 5.

## \<ok\>
printf("Good job.\n");
## \<no\>
printf("Nope.\n");
