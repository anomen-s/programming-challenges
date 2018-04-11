////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


procedure PauseThread;
begin
 TCtrl.Accessible:=false;
 repeat until TCtrl.Stopped;
end;

procedure UnpauseThread;
begin
 if (TCtrl.Content <> nil) and (TCtrl.Content^[0] <> nil) then
  TCtrl.Accessible:=true;
end;

///////////////////////////////////////////////////////////////
/// main font structure - is used for creating fonts //////////
/// lfFaceName, lfWeight and lfItalic are modified through Settings dialog
/// lfUnderline distinguishes between normal text and link
var
 DisplayLogFont: TLogFont = (lfheight:0;lfWidth:0;
 lfEscapement:0;lfOrientation:0;lfWeight:FW_DONTCARE;
 lfItalic:0;lfUnderline:0;lfStrikeOut:0;
 lfCharSet:DEFAULT_CHARSET;lfOutPrecision:OUT_DEFAULT_PRECIS;
 lfClipPrecision:CLIP_DEFAULT_PRECIS;lfQuality:DEFAULT_QUALITY;
 lfPitchAndFamily:(FF_DONTCARE or DEFAULT_PITCH);
 lfFaceName:'Times New Roman');

{////////////////////////////////////////////////////////////////////
it's called after user changes configuration in Settings dialog
/////////////////////////////////////////////////////////////////////}
procedure SetDocumentFont;
begin
 DisplayLogFont.lfItalic:=byte(ConfigInfo.Italic);

 if ConfigInfo.Bold then DisplayLogFont.lfWeight:=FW_BOLD
  else DisplayLogFont.lfWeight:=FW_DONTCARE;

 FillChar(DisplayLogFont.lfFaceName,SizeOf(DisplayLogFont.lfFaceName),0);
 Move(ConfigInfo.FontName[1],DisplayLogFont.lfFaceName, Length(ConfigInfo.FontName));

 TCtrl.NewFont:=true;
end;

///////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////

/////// returns number of words in string
function WordCount(const Txt: ANSIString): integer;
var I,C: integer;
begin
 C:=0;
 for i:=1 to Length(Txt) do
  if Txt[i] = ' ' then Inc(C);
 RESULT:=C;
end;

////// returns words from string
////// if Count = 0  returns rest of string from word Index
function GetWords(const Txt: ANSIString;Index, Count: integer): ANSIString;
var I,C: integer;
    S: ANSIString;
begin
 I:=1;C:=0;S:='';
 while (C < Index) do begin
  if (Txt[I] = ' ') then Inc(C);
  Inc(I);
 end;
 C:=0;
 if (Count = 0) then S:=copy(Txt, I, Length(Txt)-I+1)
 else
  while (C < Count) do begin
   S:=S+Txt[I];
   Inc(I);
   if (Txt[I] = ' ') then Inc(C);
  end;{while}
 I:=Length(S);
 if (S[I] = ' ') then SetLength(S,I-1);
 RESULT:=S;
end;

