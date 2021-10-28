%OUT ***** GetYear *** 
DOSSEG
.8086
RADIX 10
MODEL TINY

CODESEG
STARTUPCODE

    mov	ah, 09h		; Display program name
    mov	dx, offset PrgName
    int	21h

    mov	ax, 0c06h	; Clear Type Ahead
    mov	dl, 0FFh
    int	21h

;{ *** CMOS Year *** }
@Loop:

    mov	al, 32h		; century
    call	GetCMOS
    mov	ah, al

    mov	al, 9h		; year
    call	GetCMOS

    mov	si, offset Buffer1
    call	BCDToStr

;{ *** DOS Year *** }
    mov	ah, 2Ah
    int	21h

    mov	ax, cx
    mov	si, offset Buffer2
    call	BINToStr

; { *** Display *** }
    mov	ah, 013h
    mov	bp, offset CMOSYear
    mov	cx, 32		; length
    mov	dh, 3		; row
    mov	dl, 0		; column
    mov	bh, 0		; page num
    mov	al, 0		; subfunction
    mov	bl, 074h	; color
    int	10h

;	mov	ah, 9
;	mov	dx, offset CMOSYear
;	int	21h

;	mov	ah, 9
;	mov	dx, offset DOSYear
;	int	21h


; { Wait }
    
    xor	dx, dx
    mov	cx, 6		; time  in ticks
    mov	ah, 86h
    int	15h

; { Keypressed ? }
    mov	ah, 6
    mov	dl, 0FFh
    int	21h


    jz	@Loop

    retn
;{ ******************************************** }
;{ *********** GetCMOS ************************ }
;{********************************************* }
; In:	al = address
; Chng: -
; Out:	al = value

GetCMOS:
    out	70h, al
    in	al, 71h
    retn

;{ ***************************************** }
;{ *********** BCDToStr ******************** }
;{****************************************** }
; In:	ax = number
;       si = buffer
; Chng:	bx, si, cx
; Out:	-
BCDToStr:
    mov	cx, 4
@bcd1:
    mov	bl, '0'
    rol	ax, 4
    mov	bh, al
    and	bh, 0Fh
    add	bl, bh
    mov	ds:[si], bl
    inc	si
    loop	@bcd1
    retn
;{ ***************************************** }
;{ *********** BINToStr ******************** }
;{****************************************** }
; In:	ax = number
;       si = buffer
; Chng:	bx, si, cx
; Out:	-
BINToStr:
    mov	cx, 5
    mov	bh, 10
@bs_1:
    div	bh
    mov	bl, '0'
    add	bl, ah
    dec	si
    xor	ah, ah
    cmp	cl, 1
    je	@bs_2
    mov	ds:[si], bl
@bs_2:	loop	@bs_1
    retn

PrgName		db	0Dh, 0Ah, "GetYear", 0Dh, 0Ah, 0Dh, 0Ah,"$"
CMOSYear	db	"CMOS Year: "
Buffer1		db	"0000",0Dh,0Ah 		; ,"$"
DOSYear		db	"DOS Year:  0000"
Buffer2		db	0Dh,0Ah,"$"

END
