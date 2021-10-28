(* VersionNum: 1.10
{  **************************************************************  }
{  *                     Keyboard Library                       *  }
{  *                                                            *  }
{  * typ: INClude                                               *  }
{  *                                                            *  }
{  **************************************************************  }

FUNCTION Keypressed: boolean;
FUNCTION GetKey: char;
PROCEDURE KeybSetting(Delay, Rate: byte);
PROCEDURE ClearTA;

*)
{$IFNDEF PTN_KEYB}

{$DEFINE PTN_KEYB}

{$I keys.inc}
type
 Byte32 = array[0..31] of byte;
var
 KeybStat: word absolute    $40:$17;
 KeybBuf:  Byte32 absolute  $40:$1E;
 Keyb101:  byte absolute    $40:$96;  { and $10 = Keyb101Stat }
 KeybLED:  byte absolute    $40:$97;  { bits 0..2 = Scroll, Num, Caps }

{ *** KeyPressed *** }
FUNCTION Keypressed: boolean;assembler;
asm	mov	ax, 0B00h
	int	21h
	and	al, 1
end;

{ *** GetKey *** }
FUNCTION GetKey: char;assembler;
asm	xor	dx, dx
	jmp	@Read
@Null:	mov	dl, 80h               { set dx 128 }
@Read:	mov	ah, 8
	int	21H			{ int 21 }
	add	dl, al                { add new second key code }
	cmp	dl, 0                 { if dl = 0 ... }
	je	@Null                { ... jump @Null }
	cmp	dl, 196
	jne	@End		   { if dl = F10 ... }
	mov	ax,4CF0h
	int	21h		    { ... sudden death }
@End:	mov	al, dl
end;

{ *** KeybSetting *** }
PROCEDURE KeybSetting(Delay, Rate: byte);assembler;
asm
 mov    bl, Rate
 mov    bh, Delay
 mov    ax, 0305h
 int    16h
end;

{ *** ClearTA *** }
PROCEDURE ClearTA;assembler;
asm
 mov	ax, 0C06h
 mov	dl, 00FFh
 int	21h
end;


{$ENDIF}
