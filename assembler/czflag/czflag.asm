%OUT CZ flag
.MODEL TINY
CODESEG
.386
STARTUPCODE

FINAL   equ 0

        mov     ax, 13h
        int     10h

        push    0a000h
        pop     es
        xor     di, di

        mov     al, 0fh
@1:     mov     cx, 100*320
        rep     stosb
        sub     al, 0bh
        jns     @1

        xor     di, di
        mov     cl, 100
        mov     bx, 01ffh
        mov     al, 1
@2:     push    cx

        neg     cl
        add     cl, 101

        rep     stosb

        pop     cx
        add     di, cx
        add     di, 219
@3:
        add     cl, bl
        jz      @31
        cmp     cl, 101
        je      @31
        jmp     @2
@31:
        or      bx, bx
        js      @4
        xchg    bl, bh
        inc     cx
        jmp     @2

@4:


IFNDEF FINAL
        mov     ah, 01h
        int     21h
ENDIF
        retn
END
