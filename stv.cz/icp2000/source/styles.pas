{$I hdr.inc}
unit Styles;
interface uses Classes, Graphics;

type
 TStyleType = (stBlock, stLink, stPicture, stInline);

 PStyle = ^TStyle;
 TStyle = record
  Name: ShortString;
  SType:TStyleType;
  Size:	integer;
  case 	integer of
   0:  	(Color: TColor);
   1:	(R,G,B: byte);
 end;

function LoadStyles(const FileName: ANSIstring): TStringList;

implementation uses SysUtils, fstream;

type
  TStyleLoader = class(TDocumentStream)
  private
   NewStyleExpected: boolean;
   LStyle:	PStyle;
   LStyleName:	ShortString;
   procedure	ProcessTag(const Tag, Text: ANSIString;Embraced: boolean);
   function 	GetStyleType(const S: ANSIString): TStyleType;
   procedure	Process;
  public
   StylesList: 	TStringList;
   constructor	OpenFile(const FileName: ANSIString);
  end;


(************************************************************************
converts string style definition into more convenient
enumerated type used for parsing and displaying document
************************************************************************)
function TStyleLoader.GetStyleType(const S: ANSIString): TStyleType;
begin
 if (S = 'block') then RESULT:=stBlock
 else
  if (S = 'picture') then RESULT:=stPicture
  else
   if (S = 'fileref') then RESULT:=stLink
   else
    if (S = 'inline') then RESULT:=stInline
    else raise Exception.Create(S + ' is invalid value for field "display"');
end;

(*****************************************************************************
Checks the tags and updates style list with minimal error cheching.
Returns true if new style has been added to list.
*****************************************************************************)
procedure TStyleLoader.ProcessTag(const Tag, Text: ANSIString;Embraced: boolean);
begin
 if (Tag = ('/'+LStyleName)) then begin
  StylesList.AddObject(LStyleName, TObject(LStyle));
  NewStyleExpected:=true;
 end
 else begin
  if (Tag =  'size') then LStyle^.Size:=StrToInt(Text)
  else
   if (Tag = 'color') then LStyle^.Color:=0
   else
    if (Tag = 'red') then LStyle^.R:=StrToInt(Text)
    else
     if (Tag = 'green') then LStyle^.G:=StrToInt(Text)
     else
      if (Tag = 'blue') then LStyle^.B:=StrToInt(Text)
      else
       if (Tag = 'display') then LStyle^.SType:=GetStyleType(Text)
       else
        if (Tag[1] <> '/') then begin
         if (not NewStyleExpected) or Embraced then Error('Syntax error in style file');
         LStyle:=New(PStyle);
         LStyle^.Color:=clNone;
         LStyle^.Size:=0;
         LStyle^.Name:=Tag;
         LStylename:=Tag;
        end;{if}
  NewStyleExpected:=false;
 end;
end;

(********************************************************************
opens style file
********************************************************************)
constructor TStyleLoader.OpenFile(const FileName: ANSIString);
begin
 inherited;
 StylesList:=TStringList.Create;
end;

(********************************************************************
Goes through the file and calls ProcessTag for every Tag (except the first)
********************************************************************)
procedure TStyleLoader.Process;
var T1, T2: ANSIString;
    E: boolean;
begin
 if (ReadTag(true) <> 'style') then Error('Invalid format of style file');
 NewStyleExpected:=true;
 repeat
  T1:=ReadTag(true);
  if CheckTag then T2:='' else T2:=ReadText(true);
  E:=CheckTag and (ReadTag(false) = ('/'+T1));
  if not IsValidText(T2) then T2:='';
  ProcessTag(T1, T2, E)
 until Self.EoF;
 if (T1 <> '/style') then Error('File terminated incorrectly');
end;

///////////////////////////////////////////////////////////

(************************************************************
Loads style file and returns list of styles loaded from file
result: TStringlist: 	strings - names of styles
			objects - PStyle pointers
************************************************************)

function LoadStyles(const FileName: ANSIstring): TStringList;
var L: TStyleLoader;
begin
 L:=TStyleLoader.OpenFile(FileName);
 try
  L.Process;
 finally
  RESULT:=L.StylesList;
  L.Free;
 end;{try/f}
end;

end.

