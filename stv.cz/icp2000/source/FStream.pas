{$I hdr.inc}
unit FStream;

interface

type
 PCharArray = ^TCharArray;
 TCharArray = array[0..(MaxInt-1)] of AnsiChar;

 TOnTagEvent = procedure(Tag, Text: ANSIString;Embraced: boolean) of object;

 TDocumentStream = class(TObject)
 private
  SrcPos:	integer;
 public
  SrcSize: 	integer;
  SrcData: 	PCharArray;
  Location:	ANSIString;
  constructor	OpenFile(const FileName: ANSIString);
  destructor	Destroy;override;
 protected
  function	ReadTag(Stream: boolean):  ANSIString;
  function 	IsValidText(const Text: ANSIString): boolean;
  function	CheckTag: boolean;
  function	ReadText(Stream: boolean): ANSIString;
  function	EoF: boolean;
  procedure     Error(const Msg: ShortString);
 end;

const SpaceChars = [#09,#10,#13,' '];

function ReplaceChar(const S: ANSIString;c1,c2:char): ANSIString;

implementation uses Classes, SysUtils;

(**********************************************************************
raises EParserException to break the parsing of document
***********************************************************************)
procedure TDocumentStream.Error(const Msg: ShortString);
begin
 raise EParserError.Create(Msg);
end;

(******************************************************************
tests if current position is at the end of document
******************************************************************)
function ReplaceChar(const S: ANSIString;c1,c2:char): ANSIString;
var I: integer;
begin
 RESULT:=S;
 for I:=1 to Length(RESULT) do if (RESULT[I] = c1) then RESULT[I]:=c2;
end;


(******************************************************************
tests if current position is at the end of document
******************************************************************)
function TDocumentStream.EoF: boolean;
begin
 RESULT:=(SrcPos >= (SrcSize-1));
end;

(******************************************************************
returns true if there is a tag on current position
******************************************************************)
function TDocumentStream.CheckTag: boolean;
var P: integer;
begin
 P:=SrcPos;
 while ((SrcData[P] in SpaceChars) and (P < (SrcSize-1))) do Inc(P);
 RESULT:=((not EoF) and (SrcData[P] = '<'));
end;

(******************************************************************
reads tag from current position
******************************************************************)
function TDocumentStream.ReadTag(Stream: boolean): ANSIstring;
var S: string;
    P: integer;
begin
 P:=SrcPos;
 S:='';
 while (P < (SrcSize-1)) and (SrcData[P] in SpaceChars) do Inc(P);
  Inc(P);
  while ((SrcData[P]<>'>') and (P < (SrcSize-1))) do begin
   S:=S+SrcData[P];
   Inc(P);
  end;{while}
 if (SrcData[P] = '>') then RESULT:=S
   else RESULT:='';
 if Stream then SrcPos:=P+1;
end;

(******************************************************************
reads the text from current position up to next tag
******************************************************************)
function TDocumentStream.ReadText(Stream: boolean): ANSIString;
var P: integer;
    S: ANSIString;
begin
 P:=SrcPos;
 S:='';
 while (P < SrcSize) and (SrcData[P] <> '<') do begin
  S:=S+SrcData[P];
  Inc(P);
 end;{while}
 if Stream then SrcPos:=P;
 RESULT:=S;
end;

(**************************************************************************
OpenFile contains commof routines for descendents TDocument and TStyleLoader
**************************************************************************)
constructor TDocumentStream.OpenFile(const FileName: ANSIString);
var S: TFileStream;
begin
 inherited Create;
 Location:=ExpandFileName(FileName); //really useful function
 S:=TFileStream.Create(Location, fmOpenRead or fmShareDenyWrite);
 try
  Location:=ReplaceChar(Location,'\','/');
  SrcSize:=S.Size;
  GetMem(SrcData, SrcSize+2);
  S.Read(SrcData[0], S.Size);
  SrcData[SrcSize]:=#0;
 finally
  S.Free;
 end;{try/f}
end;

(********************************************************************
destroys TDocumentStream
*********************************************************************)
destructor TDocumentStream.Destroy;
begin
 if (SrcData <> nil) then
  try FreeMem(SrcData);
  except // don't worry, be happy...
  end;{try/e}
 inherited;
end;

(**************************************************************************
IsValidText
checks if Text contains something else than spaces, Tabs and CRLFs
**************************************************************************)
function TDocumentStream.IsValidText(const Text: ANSIString): boolean;
var L, I: integer;
begin
 L:=Length(Text);
 RESULT:=false;
 I:=1;
 while ((I <= L) and (not RESULT)) do begin
  if (not(Text[I] in SpaceChars)) then RESULT:=true;
  inc(I);
 end;{while}
end;


end.

