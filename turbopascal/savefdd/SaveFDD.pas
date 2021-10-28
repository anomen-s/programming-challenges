{  **************************************************************  }
{  *                   SaveFDD                                  *  }
{  *         program for creating disk images                   *  }
{  *                                                            *  }
{  * typ: program                                               *  }
{  *                                                            *  }
{  **************************************************************  }

Program SaveAllFDSectors;
uses Crt;
{$I Term}
{$I keyb}
var F: file;
    Data: array[0..9500] of byte;
    Track, Res: word;
    Line: word;

{$I disk}

Function IntToStr(L : LongInt) : string;
var S: string;
    N: ShortInt;
    Sign: byte;
begin
 if L < 0 then begin L:=-L;Sign:=1;end else Sign:=0;
 S[0]:=#0;
 while L <> 0 do begin
  N:=L mod 10;L:=L div 10;S:=Chr(N+$30)+S;
 end; { while }
 if S = '' then S:='0';
 if Sign <> 0 then S:='-'+S;IntToStr:=S;
end;


Procedure WriteTo(iX, iY: shortint;Msg: string);
begin
 GotoXY(iX+1, Line+iY);
 Write(Msg);
end;
Procedure ClrBuf;                  begin FillChar(Data, 9400, 0);end;

FUNCTION DiskIO(Head: byte;Track: word): byte;
var RRes, I: byte;
    SBuf: array[0..520] of byte;
begin
{ RRes:=DiskRead(Head, Track);}RRes:=SectorRead(0, Head,Track, 1,18, Data);
 DiskIO:=RRes;
 WriteTo(Track, Head, '#');
 if RRes = 0 then EXIT;
 WriteTo(Track, Head, '!');
 for I:=1 to 18 do
 repeat
    RRes:=SectorRead(0, Head, Track, I, 1, SBuf);
    if RRes = 0 then Move(SBuf, Data[(I-1)*512],512)
    else begin
     WriteTo(0,2,
       'Read Error '+IntToStr(RRes)+' at '+IntToStr(Head)+'-'+IntToStr(Track)+'-'+IntToStr(I)+', Try to read again? (y,n,q)');
     case UpCase(GetKey) of
      'N':begin FillChar(Data[(I-1)*512], 512, 0);Inc(I);end;
      'Q':begin Close(F);Halt;end;
     end; { case }
    end; { else }
 until (RRes = 0);
end;

begin
 WriteLn('Diskette saver');
 if ParamStr(1) = '' then Exit;
 Assign(F, paramStr(1));
 Rewrite(F,1);
 WriteLn('Press ESC to Exit; ENTER to continue');
 if getKey = #27 then TERM(3,'Terminated by user');
 WriteLn('Saving diskette into ',ParamStr(1)+'...');
 Write('0%                            50%                                           100%');
 WriteLn;
 WriteLn;
 Line:=WhereY-2;
 for Track:=0 to 79 do begin               { Read... }
  DiskIO(0, Track);
  BlockWrite(F, Data, 18 * 512, Res);
  if Res <> 18 * 512 then begin Close(F);TERM(6,'Write Error');end;

  DiskIO(1, Track);
  BlockWrite(F, Data, 18 * 512, Res);
  if Res <> 18 * 512 then begin Close(F);TERM(6,'Write Error');end;
 end; { for }
 WriteTo(0,3,' Done!');
end.
