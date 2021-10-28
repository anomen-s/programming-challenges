(* VersionNum: 2.10
{  **************************************************************  }
{  *                       Burning ScreenSaver                  *  }
{  *    bottom fire, burning logos, random logo colors          *  }
{  *                                                            *  }
{  * type: Program                                              *  }
{  *                                                            *  }
{  **************************************************************  }

*)


{$E-,N-}
{$Q-,R-}
procedure Sound(Hz: integer);assembler;
asm     MOV     AX, 34DDh
        MOV     DX, 0012H
        mov     bx, Hz
        CMP     DX, BX
        jae     @End
        DIV     BX
        MOV     BX, AX
        IN      AL, 61H
        TEST    AL, 3
        JNZ     @@1
        OR      AL, 3
        OUT     61H, AL
        MOV     AL, 0B6H
        OUT     43H, AL
@@1:    MOV     AL, BL
        OUT     42H, AL
        MOV     AL, BH
        OUT     42H, AL
@End:
end;

procedure NoSound;assembler;
asm     IN      AL,61H
        AND     AL,0FCH
        OUT     61H,AL
end;

{ *** Wait *** }
Procedure Wait;
var _Stop: LongInt;
    TimerTick:  LongInt absolute $40:$6C;
begin
 _Stop:=TimerTick+1;
 repeat until Timertick >= _Stop;
end;

{ *** KeyPressed *** }
FUNCTION Keypressed: boolean;assembler;
asm     mov     ax, 0B00h
        int     21h
        and     al, 1
end;

{ *** GetKey *** }
FUNCTION GetKey: char;assembler;
asm     xor     dx, dx
        jmp     @Read
@Null:  mov     dl, 80h               { set dx 128 }
@Read:  mov     ah, 8
        int     21H                     { int 21 }
        add     dl, al                { add new second key code }
        cmp     dl, 0                 { if dl = 0 ... }
        je      @Null                { ... jump @Null }
        mov     al, dl
end;

{ *** ClearTA *** }
PROCEDURE ClearTA;assembler;
asm
 mov    ax, 0C06h
 mov    dl, 00FFh
 int    21h
end;

procedure SetMode13;inline($B8/>$13/$CD/$10);{mov ax, 13h;int 10h}
procedure SetMode3;inline($B8/>$03/$CD/$10);{mov ax, 3h;int 10h}

procedure ShowFakeScreen(Segment: word);assembler;
asm     push    ds
        mov     es, [SegA000]
        mov     ds, [Segment]
        xor     di, di
        xor     si, si
        mov     cx, 320 * 200 / 4
db 66h; rep     movsw
        pop     ds
end;

procedure FFillScreen(Segment: word;Color: byte);assembler;
asm     mov     al, Color       { set eax }
        mov     ah, al
        mov     dx, ax
db 66h; shl     ax, 16
        mov     ax, dx
        mov     es, [Segment]   { set es:di }
        xor     di, di
        mov     cx, 65520       { set count }
db 66h; rep     stosw           { write }
end;

function  CreateFakeScreen(var FakeSeg: word): boolean;
var FakeScr:    pointer;
    Result:     boolean;
begin
 Result:=(MaxAvail > 65528);
 CreateFakeScreen:=Result;
 if not Result then Exit;
 GetMem(FakeScr, 65528);
 FakeSeg:=(longint(FakeScr) shr 16);
 if word(FakeScr) <> 0 then Inc(FakeSeg);
 FFillScreen(FakeSeg,0);
end;


procedure FPutPixel(Segment: word;X, Y: word;Color: byte);assembler;
asm     mov     di, [Y] { offset }
        mov     dx, di
        shl     di, 6
        shl     dx, 8
        add     di, dx
        add     di, [X]
        mov     es, [Segment]
        mov     al, [Color]

        stosb
end;

procedure CopyMaskBitmap(var Src;Dest: word;Width, Height, X, Y: word; Mask: byte);assembler;
asm     push    ds
        cld
        mov     di, [Y]        { es:di }
        add     di, [Height]
        dec     di
        mov     dx, di
        shl     di, 8
        shl     dx, 6
        add     di, dx
        add     di, X
        mov     es, Dest
        lds     si, Src         { ds:si }
        mov     bx, [Height]
        mov     dx, 320
        add     dx, [Width]             { dx:=320-Width }
        mov     ah, [Mask]
@1:     mov     cx, [Width]
@2:     lodsb
        or      al, ah
        jz      @3
        mov     es:[di], al{stosb}
@3:     inc     di
        dec     cx
        jnz     @2
        sub     di, dx
        dec     bx
        jnz     @1

        pop     ds
end;
procedure CopyBitmapShade(var Src;Dest: word;Width, Height, X, Y: word;Color: byte);assembler;
asm     push    ds
        cld
        mov     di, [Y]        { es:di }
        add     di, [Height]
        dec     di
        mov     dx, di
        shl     di, 8
        shl     dx, 6
        add     di, dx
        add     di, X
        mov     es, Dest
        lds     si, Src         { ds:si }
        mov     bx, [Height]
        mov     dx, 320
        add     dx, [Width]             { dx:=320-Width }
        mov     ah, [Color]
@1:     mov     cx, [Width]
@2:     lodsb
        or      al, 0
        jz      @3
        mov     es:[di], ah{stosb}
@3:     inc     di
        dec     cx
        jnz     @2
        sub     di, dx
        dec     bx
        jnz     @1

        pop     ds
end;


PROCEDURE SetPal(Index : Byte; R, G, B: Byte);assembler;
asm     mov     dx, 3C8h        {  Port[$3c8] := ColorNo; }
        mov     al, [Index]
        out     dx, al
        inc     dx              {  Port[$3c9] := R; }
        mov     al, [R]
        out     dx, al
        mov     al, [G]         {  Port[$3c9] := G; }
        out     dx, al
        mov     al, [B]         {  Port[$3c9] := B; }
        out     dx, al
end;

PROCEDURE VertRetrace;
inline($BA/$3DA/        {       mov     dx, 3DAh }
       $EC/             { @1:   in      al, dx }
       $A8/$08/         {       test    al, 8 }
       $74/$FB);        {       je      @1 }

procedure burn(Segment:word);assembler;
asm
        mov     es, [Segment]
        mov     di, 320*200
@1:     xor     ax, ax
        mov     dx, ax
        dec     di
        mov     dl, es:[di]
        mov     al, es:[di+319]
        add     dx, ax
        mov     al, es:[di+320]
        add     dx, ax
        mov     al, es:[di+321]
        add     dx, ax
        shr     dx, 2
        mov     es:[di], dl
        or      di, di
        jnz     @1
end;

procedure FDrawHLine(Segment: word;Xs, Ys, Len: word;Color: byte);assembler;
asm     mov     di, [Ys]        { offset }
        mov     dx, di
        shl     di, 6
        shl     dx, 8
        add     di, dx
        add     di, [Xs]
        mov     es, [Segment]
        mov     cx, Len
        mov     al, [Color]
        rep     stosb
end;

procedure Filter(Segment, R1: word);assembler;
asm     mov     es, [Segment]
        xor     di, di
        mov     dx, R1
@1:     mov     al, es:[di]
        cmp     al, 0f8h
        jb      @2
        xor     dx, di
        sub     ax, dx
        xor     al, 07h
        or      al, 0F8h
        mov     es:[di], al
@2:     inc     di
        cmp     di, 320*200
        jb      @1
end;
procedure MergeToMax(DestSeg, SrcSeg: word);assembler;
asm     push    ds
        mov     es, [DestSeg]
        mov     ds, [SrcSeg]
        xor     di, di
        xor     si, si
@1:     mov     dl, es:[di]
        lodsb
        cmp     al, dl
        ja      @2
        xchg    al, dl
@2:     stosb
        cmp     di, 320*200
        jb      @1
        pop     ds
end;

procedure FRectangle(Segment, Xs, Ys, Xe, Ye: word;Color: byte);
var x, y: word;
begin
  x:=xe-xs+1;
  for Y:=Ys to Ye do
   FDrawHLine(Segment, xs, y, x, Color);
end;

Procedure LogoPic;external;
{$L logopic.obj}
{ Colors:
 points F4 = dark gray $202020
 back   00 = black
 email  F6 = blue/green $002020
 logo   F8-ff = blue ($3F)
}

type
 TPicture = record
            x, y:       integer{word};
            dx, dy:     integer;
           end;

const
 MaxPics = 100;

 ShowFire: boolean = true;
 PicsCount: byte = 2;           { start with one logo }
 D1:    integer = 1;            { color shift 1 }
 Pal_G: byte    = $20;
 counter: byte  = 0;
var Pics: array[0..MaxPics] of TPicture;
    i: integer;
    FireSeg, FakeSeg, ShadeSeg, w: word;
type    VGA = array[0..63999] of byte;
begin
 if not (CreateFakeScreen(FakeSeg) and CreateFakeScreen(FireSeg) and CreateFakeScreen(ShadeSeg)) then
  begin WriteLn('Not enough memory');end;
 SetMode13;
 for I:=0 to $7F do SetPal(I, (I shr 1), 0, 0);
 for I:=$F8 to $fF do SetPal(I, 0, $20 - ((I and $F) shl 1), $3f+$8-(I and $0F));
 SetPal($F4, $20,$20,$20);{ 3 pixels below letter 'N' }
{ SetPal(0,0,$3f,0); {green background - for testing}

 Randomize;
 Pics[0].X:=150;Pics[0].Y:=100;
 Pics[0].dX:=1;Pics[0].dY:=1;
 repeat
 FDrawHLine(ShadeSeg,0,200,320,0);
  if ShowFire then      for I:=0 to 320 do FPutPixel(FireSeg, I, 200, Random($80))
  else                  FDrawHLine(FireSeg,0,200,320,0);

  for I:= 0 to (PicsCount-1) do         { draw shade }
   CopyBitMapShade(byte(@LogoPic^), ShadeSeg, 80,45, Pics[I].X, Pics[I].Y, Random($50)+$30);
{  if ShowFire then begin                { fire effect }
   burn(FireSeg);burn(ShadeSeg);
   Move(ptr(FireSeg, 0)^, ptr(FakeSeg,0)^, 320*200);
   MergeToMax(FakeSeg, ShadeSeg);
(*  end{if}
  else FFillScreen(FakeSeg, 0);
  *)
  for I:= 0 to (PicsCount-1) do begin   { draw logos }
   CopyMaskBitmap(byte(@LogoPic^), FakeSeg, 80, 45, Pics[I].X, Pics[I].Y, 0);
   if ((counter and $3) = 0) then
    with Pics[I] do begin               { change movement }
     dx:=Random(11)-5;
      if ((x < 10) and (dx < 0)) then Inc(dx, 3);
      if ((x > 230) and (dx > 0)) then Dec(dx, 3);
     dy:=Random(11)-5;
      if ((y < 10) and (dy < 0)) then Inc(dy, 3);
      if ((y > 145) and (dy > 0)) then Dec(dy, 3);
    end;{with}                             { move logos }
   Pics[I].X:=Pics[I].X+Pics[I].dx;Pics[I].Y:=Pics[I].Y+Pics[I].dy;
  end;{for}
  Inc(Counter);
                                        { palette rotation }
  if (Pal_G > $3E) then D1:=-1 else if (Pal_G < $8) then D1:=1;
   Inc(Pal_G, D1);SetPal( $F6, 0, Pal_G, Pal_G);

  Filter(FakeSeg, Random($FFFF));
  VertRetrace;                          { show screen }
  ShowFakeScreen(FakeSeg);

  if Keypressed then begin              { read key }
   case UpCase(GetKey) of
    'A': if (PicsCount < MaxPics) then begin
           Inc(PicsCount);
           with Pics[PicsCount-1] do begin
             X:=100;Y:=50;
             dX:=1;dY:=1;
           end;{with}
         end {if}
         else
          begin Sound(50);ClearTA;Wait;nosound;end;
    'D': if (PicsCount > 0) then Dec(PicsCount);
    'S': ShowFire:=not ShowFire;
    #27, #13: begin SetMode3;EXIT;end;
   end;{case}
  end;{if}
  ClearTA;Wait;

 until false;
end.
