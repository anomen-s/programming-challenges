{  **************************************************************  }
{  *                   SaveBoot                                 *  }
{  *                                                            *  }
{  * typ: program                                               *  }
{  *                                                            *  }
{  **************************************************************  }
{$G+}

FUNCTION BootSectorRead(Drive: byte;var P): byte;assembler;
asm	les	bx, P
    mov	ah, 2   	{ Func number }
    mov	al, 1		{ sector count <= sectors/track }
    mov	dl, Drive	{ drive }
    mov	dh, 1		{ povrch / head / side 0..x }

    mov	cx, 0		{ stopa / cylinder(track) 10-bit = 0..1023 }
    xchg	cl, ch
    shl	cl, 6           { CH = tttttttt   CL = TtSsssss }
    add	cl, 1		{ sector 6-bit 1..n }

    int	13h
{ jc	@Error;	xor	ah, ah;	@Error:}
    mov	al, ah
end;

var
    f: file;
    Data: array[0..600] of byte;
    RES: word;

begin
 WriteLn('HDD Boot sector saver');

 Assign(F, 'BootC'); Rewrite(F, 1);
 WriteLn(BootSectorRead(128, Data));
 BlockWrite(F, Data, 512, Res);
 Close(F);
 if (Res <> 512) then begin WriteLn('Write Error');end;

 Assign(F, 'BootD'); Rewrite(F, 1);
 WriteLn(BootSectorRead(129, Data));
 BlockWrite(F, Data, 512, Res);
 Close(F);
 if (Res <> 512) then begin WriteLn('Write Error');end;
end.

