{  **************************************************************  }
{  *                  Disk Access Library                       *  }
{  *                                                            *  }
{  * typ: INClude                                               *  }
{  *                                                            *  }
{  **************************************************************  }

FUNCTION SectorRead(Drive, Head: byte;Track: word;Sector, Number: byte;var P): byte;assembler;
asm	les	bx, P
	mov	ah, 2   	{ Func number }
	mov	al, Number	{ sector count <= sectors/track }
	mov	dl, Drive	{ drive }
	mov	dh, Head	{ povrch / head / size 0..x }

	mov	cx, Track	{ stopa / cylinder(track) 10-bit = 0..1023 }
	xchg	cl, ch
	shl	cl, 6           { CH = tttttttt   CL = TtSsssss }
	add	cl, Sector	{ sector 6-bit 1..n }

	int	13h
{ jc	@Error;	xor	ah, ah;	@Error:}
	mov	al, ah
end;
(*
FUNCTION DiskRead(Head: byte;Track: word): byte;assembler;
asm	mov	bx, offset Data
	mov	ah, 02		{ Func number }
	mov	al, 18		{ sector count <= sectors/track }
	mov	dl, 0		{ drive }
	mov	dh, Head	{ povrch / head / size 0..x }

	mov	cx, Track	{ stopa / cylinder(track) 10-bit = 0..1023 }
	xchg	cl, ch
	shl	cl, 6           { CH = tttttttt   CL = TtSsssss }
	inc	cx		{ sector 6-bit 1..n }
	int	13h
	mov	al, ah
end;
  *)