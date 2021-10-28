model small
.386
.data
ends

.code
startupcode

public Loader

Loader:
        nop
        nop
        mov     ax,cs           ; calculate segments
        sub     ax,00010h
        mov     ds,ax           ;set ds
        mov     ss,ax           ;set ss
        mov     fs,ax
        mov     gs,ax

        xor     ax,ax           ; push 0000
        mov     word ptr ds:[0FFFEh], ax

        push    ds              ; jump to start
        push    00100h
        retf

        nop
        nop
        nop
        nop
        nop
        nop
        nop
ends

end
