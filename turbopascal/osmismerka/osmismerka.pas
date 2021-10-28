{$G-,Q-,R-}
uses Crt, TPStr;
{$M 8000, 0, 0}
{$I keys.inc}
{DEFINE Line50}
const MaxX = 40;
      LastLine =
{$IFDEF Line50} 50;
{$ELSE}         25;
{$ENDIF}
type TScr = array[1..LastLine,1..MaxX] of record Ch:char;Color:byte;end;
var
 Scr:   TScr absolute $B800:0;
 WScr:  array[1..25,1..40] of word absolute $B800:0;
 X, Y:  byte;
 Word:  string;

{ *** GetKey *** }
Function GetKey : char;assembler;
const F10       = #196; { funkcni klic 10 }
 asm
  mov  dl,0;
  jmp  @Read;
 @Null:
  mov  dl,$80;               { set dx 128 }
 @Read:
  mov  ah,8;    int  21H;    { int 21 }
  add  dl,al;                { add new second key code }
  or    dl,dl                { if dl = 0 ... }
  jz   @Null;                { ... jump @Null }
  cmp  dl,F10;  jne  @End;   { if dl = F10 ... }
  mov   ax,83h; int  10h;
  mov  ax,$4CF0;int  $21;    { ... sudden death }
 @End:
  mov al,dl;
end;

Function SearchDirection(XS, YS, XD, YD: shortint;SWord: string): boolean;
var L :byte;
    Ok:boolean;
begin
 Ok:=true;
 for L:=2 to Ord(SWord[0]) do  { delka slova }
  if Ok and (XS+XD in [1..MaxX]) and (YS+YD in [2..LastLine]) then
  begin
   Inc(XS,XD); Inc(YS,YD);
   if Scr[YS, XS].Ch <> SWord[L] then Ok:=false;
  end else Ok:=false;
  SearchDirection:=Ok;
end;

Procedure Fill(XS, YS, XD, YD, Len: ShortInt);
var L:byte;
begin for L:=1 to Len do begin Scr[YS, XS].Color:=1;Inc(XS, XD);Inc(YS, YD);end;end;

Function Search(SWord: string): boolean;
const Directs : array[1..8] of record X,Y:shortint;end =
        ((X: 0;Y:-1),(X: 1;Y:-1),(X: 1;Y: 0),(X: 1;Y: 1),(X: 0;Y: 1),(X:-1;Y: 1),(X:-1;Y: 0),(X:-1;Y:-1));
var XS, YS, D : byte;
    Ok: boolean;
begin
 for Xs:=1 to MaxX do
  for Ys:=2 to LastLine do
   if Scr[YS, XS].Ch = SWord[1] then
    for D:=1 to 8 do   { smery }
    begin
     Ok:=SearchDirection(XS, YS, Directs[D].X, Directs[D].Y, SWord);
     if Ok then
     begin
      Fill(XS, YS, Directs[D].X, Directs[D].Y,Ord(SWord[0]));
      Scr[1,MaxX].Ch:='ű';
      Search:=true;exit;
     end;
    end;
 Sound(1000);
 Delay(80);
 NoSound;
 Search:=false;
end;

Procedure Write(X,Y:byte;S:string);
var L:byte;
begin
 for L:=1 to Ord(S[0]) do
 begin
  if (X in [1..MaxX]) and (Y in [1..LastLine]) then Scr[Y,X].Ch:=S[L];
  Inc(X);
 end;
end;

Procedure Edit;
var Key: char;
begin
 X:=1;Y:=2;Key:=#0;
 while Key <> Esc do
 begin
  GoToXY(X,Y);Key:=UpCase(GetKey);
  case Key of
   Left: if X > 1 then Dec(X);                { Movement keys }
   Right:if X < MaxX then Inc(X);
   Tab:  if X < MaxX-7 then Inc(X,8);
   BS:   if X > 1 then Dec(X) else if Y > 2 then begin X:=MaxX;Dec(Y);end;
   Home: X:=1;
   EndK: X:=40;
   Up:   if Y > 2 then Dec(Y);
   Down: if Y < LastLine then Inc(Y);
   PgDn: Y:=LastLine;
   PgUp: Y:=2;
   CR:   if Y < LastLine then begin Inc(Y);X:=1;end;
   Ins:  Scr[Y,X].Color:=Scr[Y,X].Color xor $E;
   #32..#255: begin Scr[Y,X].Ch:=Key;if X < MaxX then Inc(X) else if Y < LastLine then begin X:=1;Inc(Y);end;end;
  end;
 end;
end;
        { ****** M A I N   P R O G R A M ****** }
begin
{$IFDEF Line50}
 TextMode(CO40+Font8x8);
{$ELSE}
 TextMode(CO40);
{$ENDIF}
 ClrScr;
 for X:=1 to MaxX do for Y:=2 to LastLine do WScr[Y, X]:=$F20;
 for X:=1 to MaxX do WScr[1,X]:=$7020;
 Write(5,1,'Osmismerka snadno a rychle!');
 EDIT;
 GoToXY(1,1);
 for X:=1 to MaxX do WScr[1,X]:=$7020;
 Word:=' ';
 repeat
  GoToXY(1,1);
  repeat until KeyPressed;for X:=1 to MaxX-1 do WScr[1,X]:=$7020;
  ReadLn(Word);Sound(5000);Delay(1);NoSound;
  if Word = '' then begin EDIT;{GoToXY(1,1);ReadLn(Word);}end;
  if Word <> '' then if not Search(UpStr(Word)) then Scr[1,MaxX].Ch:='-';
 until false;
end.
