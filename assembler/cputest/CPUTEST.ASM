%OUT *** 386 CPU Tester ***
.MODEL TINY	; use Tiny model - data, code & stack in one segment
CODESEG
.286
STARTUPCODE	; space for Program Segment Prefix

@8086:	push	sp		; 8086 test
	pop	ax
	cmp	ax, sp
	jne	@Not386

@Real:	mov	ax, 0FFFFh
	mov	cl, 20h
	shl	ax, cl
	or	ax, ax
	jz	@Not386

; ******** 386 Installed ********
	ret

@Not386:
	mov	ax, 9
	mov	dx, offset NoCPU
	ret

NoCPU	db	"This program requires 80386 or better processor.",0Ah, 0Dh, "$"
end
