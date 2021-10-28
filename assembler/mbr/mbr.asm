; build using:
; tasm /zi /t /m4 mloader.asm
; tlink /tdc /m /s /l mloader.obj


; Master Boot Loader
; last edit: 2003-08-30: working.
; mod: 2005-12-24: removed option 0
; mod: 2006-01-07: SectorShift
;
debug		EQU	0	; debugging - 0=NO
radix 10                        ;             1=YES
model tiny
codeseg
.386		; we want 32-bit registers
startupcode

MenuItemLength	EQU	0010h

ImgBase		EQU	0600h

BootBase	EQU	7C00h

IF debug EQ 0
    COMBase EQU	0500h
    PSPBase	EQU	0100h
ELSE
    COMBase	EQU	0600h-7c00h
    PSPBase	EQU	7c00h

    JMP	@Init
    ORG 	BootBase
    @Init:
ENDIF

IF debug NE 0
 IF debug NE 1
  mov ax, invalid_debug_value  ; debug must be either 1, or 0
 ENDIF
ENDIF

; ************************************************************
;       Move Master Boot Sector from  0000:7C00 to 0000:0600
;		BootBase --> ImgBase
; ************************************************************

    cli			
    xor	ax, ax          ; loaded at 0000:7C00
IF debug EQ 0
    mov	ss, ax          ; SS = DS = ES = 0000
    mov	es, ax
    mov	ds, ax
ENDIF
    mov	sp, BootBase    ; SP = 7C00
    mov	si, sp
    sti
    cld
    mov	di, ImgBase	; DS:SI = 0000:7C00 --> ES:DI = 0000:0600
    mov	cx, 0100h	; move 512 byte
    repnz   movsw	
IF debug EQ 1
    mov	ax, cs
    mov	cs:word ptr [BootSeg], ax
ENDIF
    db	0EAh            ; JMP	0000:0620
    dw	ComBase+offset CodeEntry		
BootSeg	dw	0

; CS = DS = ES = SS = 0000
; SP = 7C00
; IP = 06xx
; DI = 0800
; SI = 7E00
; AX = CX = 0000
; ************************************************************
;        Print menu
; ************************************************************
CodeEntry:
    mov	si, COMBase + offset SelectMBR
    Call	Print

    mov	si, COMBase + offset Menu   ; first menu item
    xor	al, al
PrintMenu:
    push	si			; print number
    mov	si, COMBase + offset MenuNumberStr
        call	Print
    inc	byte ptr [COMBase + offset MenuNumber]  ; inc menu number
    pop	si
    push	si
        call	Print ; print menu title
    pop	si
    add	si, MenuItemLength ; next menu title
    inc	al        ; menu items
    cmp	byte ptr [si],0      ; print next menu item ?
    jnz	PrintMenu

    add	al, '0'			; save number of menu items for keypress check
;	mov	byte ptr [COMBase + offset MenuItems],al
    mov	ch, al
    
    mov	si, COMBase + offset CRLF
        call	Print

; ************************************************************
;        User Boot Partition Selection
; ************************************************************

IF debug EQ 1
    push	0
    pop	ds
ENDIF
    mov	edx, dword ptr [ds:046Ch]        ; start time
WaitForKey:
IF debug EQ 1
    push	0
    pop	ds
ENDIF
    mov	eax, dword ptr [ds:046Ch]        ; current time
IF debug EQ 1
    push	es
    pop	ds
ENDIF
    sub	eax, edx                         ; elapsed time
    mov	cl, byte ptr [COMBase + offset TimeShift]
    shr	eax, cl
    mov	al, byte ptr [COMBase + offset DefaultItem]	; sectornumber
    jnz	TimeOff
    mov	ah, 11h
    int	16h
    jz	WaitForKey
ReadKey:			; key input
    mov	ah, 10h
    int	16h
    mov	byte ptr [COMBase + offset MenuNumber], al      ; print key
    mov	si, COMBase + offset MenuNumber
    call	Print
    cmp	al, '0'  
    jbe	ReadKey  	; MOD: 2005-12-24: do not accept 0
        cmp	al, ch
    ja	ReadKey
    
TimeOff:
    mov	byte ptr [COMBase + offset MenuNumber], '1'  ; reset changes

    sub	al, ('0' - 1)  ; '0' => 0x1, '1' => 0x2, '2' => 0x3,...

; *** LAST *** -- not enough space
;	mov	si, COMBase + offset LastConfig
;	push	si
;	pop	di
;	cmp	al, 1	
;	ja	PTScanFinished
;	lodsb
;	mov	byte ptr [COMBase + offset LastConfig], al 
;InputDone:
             ; we are working in 0000:0600
; ************************************************************
;        Load Selected Sector at 0000:7c00h
; In: CX = partion cyl/sec
; ************************************************************
PTScanFinished:      
;	stosb
;	mov	byte ptr [COMBase + offset LastConfig], al ; save last 

;	mov	al, byte ptr [COMBase + offset SectorShift] 
    movzx	cx, al		; sectornumber

    mov	dx, 0080h	; head /drive
Reading:mov	bx, BootBase	; buffer ES:BX = 0000:7C00
    mov	ax, 0201h	; function read / 1 sectors
    int	13h		; Diskette Function Call
    jnc	DoPTCompare	; jump if OK
    xor	ax, ax		; AH = function reset HDC
    int	13h		; Diskette Function Call
    mov	si, COMBase + offset ReadSectorErr
    call	Print
    mov	ah, 10h
    int	16h
    jmp	Reading

; check PT at (ImgBase) 0000:0600 and (BootBase) 0000:7C00
DoPTCompare:
    mov	si, BootBase+1beh
    mov	di, ImgBase+1beh
        mov	cx, 0042h        ; 4*16+2

    push	cx si di
    repe	cmpsb
    pop	di si cx

;DoSectorWrite:
; ************************************************************
;         Rewrite PT in MBR and write MBR (0000:0600) back
; ************************************************************

    je	RunMBR
        
    cld
    repnz   movsb	; PT(0000:7c00) -> PT(0000:0600)

    mov	cx, 1		; track / sector
    mov	dx, 0080h	; head /drive
    mov	bx, ImgBase	; buffer ES:BX = 0000:0600
    mov	ax, 0301h	; function write / 1 sectors
    int	13h		; Diskette Function Call
    jnc	SectorWritten	; jump if OK
    mov	si, COMBase + offset WriteSectorErr
    Call	Print
SectorWritten:
    mov	si, COMBase + offset MBRWriting
    Call	Print

RunMBR:

; ************************************************************
;         Run MBR
; ************************************************************

    push	7c00h
    retn

; ************************************************************
;        Print ASCII-Z Error Message
; In: SI = offset of message
; ************************************************************
Print:  push	ax bx
Prn000:	lodsb			; al = char
    or	al, al
    jz	Prn001
    push	si
    mov	bl, 007h	; bl = color
    mov	ah, 0Eh		; ah = function write char
    int	10h		; Video Function Call
    pop	si
    jmp	Prn000
Prn001:	pop	bx ax
    ret
; ************************************************************

SelectMBR	db	"Select configuration:",0Dh,0Ah ,00h
;		db	"0. last", 00h -- removed as function "previous-choice" is not implemented
CRLF		db	0Dh, 0Ah, 20h, 00h
ReadSectorErr	db	0dh,0ah,"PT: Error reading from disk",00h
WriteSectorErr	db	0dh,0ah,"PT: Error writing to disk.", 00h
MBRWriting	db	"*", 0
MenuNumberStr	db	0Dh, 0Ah
MenuNumber	db	"1. ",0   ; used as buffer for printing numbers
;LastConfig	db	0
SectorShift	db	0 ; number of empty sector between mbr and first OS mbr

    ; Data	ASCII-Z strings max. length 16 bytes - description of choices
ORG	PSPBase + 015Bh

Menu	db	"windows 95     ",0  ;15B
    db	"Linux          ",0  ;16B
    db	"windows 2000   ",0  ;17B
    db	"windows NT     ",0  ;18B
;	db	"red hat linux  ",0  ;19B
;	db	"suse linux     ",0  ;1AB
    db	0 ; menu stop        ;1BB

ORG PSPBase + 01BCh
DefaultItem	db	'1'
TimeShift	db	5

; PT: 1BEh, 1CEh, 1DEh, 1EEh

ORG PSPBase + 01FEh
BootSign	DB	055h,0AAh				;002FE

END


