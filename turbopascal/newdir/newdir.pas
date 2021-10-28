uses dos;
Function IntToStr(L : byte) : string;
var S:string;
begin
  S[0]:=#2;
  S[1]:=chr( ((L div 10) mod 10) + ord('0') );
  S[2]:=chr( (L mod 10) + ord('0'));
  IntToStr:=S;
end;


var Y, M, D, W: word;
    Name: string[8];
    Rec: SearchRec;
begin
 GetDate(Y, M, D, W);
 Name:=IntToStr(Y-1900)+'_'+IntToStr(M)+'_'+IntToStR(D);
 { Y2K compatibility }
 if Y >= 2000 then Name[1]:=char(byte(Name[1])+$31);
 WriteLn('--- ',Name,' ---');
 FindFirst(Name, AnyFile, Rec);
 if (DOSError = 0) and (Rec.Name = Name) then begin
   WriteLn('Adresar jiz existuje');
   Halt;
 end; { if }
 MkDir(Name);
end.
