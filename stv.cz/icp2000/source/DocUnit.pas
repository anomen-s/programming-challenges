{$I hdr.inc}
unit DocUnit;

interface
uses Classes, Controls, Graphics,  Forms, StdCtrls,
     FStream, Styles;

type
  TSourceForm = class(TForm)
    Memo1: TMemo;
    procedure FormKeyPress(Sender: TObject; var Key: Char);
  end;

const
 MaxPointerIndex = (MaxInt div 8);

const
 ptrBreak = nil;

type
 TPartType = (ptText, ptPicture);

 PDocPart = ^TDocPart;
 TDocPart = record
  Index: integer;
  Link:	 ANSIString;
  Text:	 ANSIString; // ANSIstr can't be in variant part
  case PType: TPartType of
   ptText:      (Color: TColor;FontSize: byte);
   ptPicture:	(Image: TBitmap);
 end;

 PDocParts = ^TDocParts;
 TDocParts = array[0..MaxPointerIndex] of PDocPart;

 TDocument = class(TDocumentStream)
  private
   FCount:      integer;
   Styles:	TStringList;
   FCapacity:   integer;
   LoaderMaxI:	integer;
   Links:	TStringList;
   function	IndexOfStyle(const S: ShortString): integer;
   procedure    AllocateNew;
   procedure    Add(Style: PStyle;const Text: ANSIString;Index: integer);
   procedure	AddBreak;
   procedure	CreateLinksAndLines;
   function	Process(ParentStyle: PStyle;const SelfTag: ANSIString): ANSIString;
   function 	GetLink(const Text: ANSIString): ANSIString;
   function	OpenPicture(const FileLocation: ANSIString): TBitmap;
   function	FormatText(const Text: ANSIString): ANSIString;
  public
   FContent:    PDocParts;
   constructor	OpenFile(const FileName: ANSIString);
   destructor	Destroy;override;
   procedure	ShowSource;
 end;

implementation uses SysUtils, config;
{$R *.DFM}


(***********************************************************************
displays form with document source
********************************************************************)
procedure TDocument.ShowSource;
var F: TSourceForm;
begin
 F:=TSourceForm.Create(Application.MainForm);
 F.Caption:=Self.Location;
 if (Self.SrcSize > 0) then
  F.Memo1.Lines.SetText(PChar(SrcData));
 F.ShowModal;
 F.Free;
end;


procedure TSourceForm.FormKeyPress(Sender: TObject; var Key: Char);
begin
 if (Key =#27) then Close;
end;

///////////////////////////////////////////////////////////////////

const AllocBy = 64;

{ *** AddBSlash *** }
function AddBSlash(const FName: ANSIString): ANSIString;
begin
 RESULT:=FName;
 if (FName <> '') and (FName[Length(FName)] <> '\') then
   RESULT:=RESULT+'\';
end;

////////////////////////////////////////////////////////////////
(**********************************************************************
returns the expanded link location
**********************************************************************)
function TDocument.GetLink(const Text: ANSIString): ANSIString;
var P: ANSIString;
begin
 P:=AddBSlash(ExtractFilePath(ReplaceChar(Location,'/','\')))
       +ReplaceChar(Text,'/','\');
 RESULT:=ExpandFileName(P);
end;

(*************************************************************************
tries to open the picture and return it as TBitmap
if fails (file doesn't exists or has unknown format) the result
is alternative picture (small icon and the location of file with picture)
*************************************************************************)
function TDocument.OpenPicture(const FileLocation: ANSIString): TBitmap;
var P: TPicture;
    B: TBitmap;
begin
 P:=TPicture.Create;
 B:=TBitmap.Create;
 try
  P.LoadFromFile(GetLink(FileLocation));	// loading file from disk
  B.Width:=P.Width;
  B.Height:=P.Height;
  B.Canvas.Draw(0,0,P.Graphic);
 except
  P.Bitmap.LoadFromResourceName(hinstance,'SHAPES'); // something failed
  P.Bitmap.Transparent:=true;			// so we have to create
  B.Width:=B.Canvas.TextWidth(FileLocation)+48;	// alternative image
  B.Height:=38;
  B.Canvas.Brush.Color:=ConfigInfo.BGColor;
  B.Canvas.FillRect(Rect(0,0,B.Width,38));
  B.Canvas.RoundRect(0,0,B.Width,38,10,10);
  B.Canvas.TextOut(38,((36-B.Canvas.TextHeight(FileLocation)) shr 1)+1, FileLocation);
  B.Canvas.Draw(3, 3, P.Bitmap);
 end;{try/e}
 P.Free;
 RESULT:=B;
end;

(***********************************************************************
returns 'special' character converted from symbol in Symbol[Index]
********************************************************************)
Function ReplaceSymbol(const Symbol: ANSIString;var Index: integer): ANSIString;
var S: ShortString;
    L: integer;
begin
  if (Symbol[Index] <> '&') then raise EParserError.Create('Cannot replace symbol');
  S:='';L:=Length(Symbol);Inc(Index);
  while ((Symbol[Index] <> ';') and (Index <= L)) do begin
   S:=S+Symbol[Index];
   Inc(Index);
  end;{while}
  if (S = 'lt') then RESULT:='<'
  else
    if (S = 'gt') then RESULT:='>'
    else
     if (S = 'amp') then RESULT:='&'
     else RESULT:='&'+S+';';
end;

(*************************************************************************
formats text -
  removes redundant spaces, replaces &amp; and &lt; with '&' and '<'
**********************************************************************)
function TDocument.FormatText(const Text: ANSIString): ANSIString;
var I, L: integer;
    S: ANSIString;
begin
 S:='';L:=Length(Text);I:=1;
 while (I <= L) do begin
  case Text[I] of
   '&': S:=S+ReplaceSymbol(Text, I);
   #09,#10,#13,' ': if ((S <> '') and (not (S[Length(S)] in SpaceChars))) then S:=S+' ';
   '<': Error('Unexpected Tag');
   else S:=S+Text[I];
  end;{case}
 Inc(I);
 end;{while}
 if (S[Length(S)] <> ' ') then S:=S+' '; // this is for GetWord in Display.pas
 RESULT:=S;
end;		// result must have format 'word_1 word_2 word_n '


destructor TDocument.Destroy;
var I: integer;
begin
 for I:=0 to (FCount-1) do begin // free all doc parts
  if FContent^[i] <> nil then begin
   FContent^[i]^.Text:='';
   FContent^[i]^.Link:='';
   if (FContent^[I]^.PType = ptPicture) then FContent^[i]^.Image.Free;
  end;{if}
  FreeMem(FContent^[I]);
 end;{for}
 FCount:=0;
 ReallocMem(FContent, 0);
 inherited;
end;

(***********************************************************
chechs size of FContent and allocates more memory if needed
************************************************************)
procedure TDocument.AllocateNew;
var NewCapacity: integer;
begin
 NewCapacity:=FCount + AllocBy;
 if (FCapacity < NewCapacity) then begin
  ReallocMem(FContent, NewCapacity * SizeOf(PDocPart));
  FCapacity:=NewCapacity;
 end;
end;


procedure TDocument.AddBreak;
begin
 if ((FCount > 0) and (FContent^[FCount-1] <> ptrBreak)) then begin
  if (FCount >= (FCapacity-1)) then AllocateNew;
  FContent^[FCount]:=ptrBreak;
  Inc(FCount);
 end;{if}
end;

(**************************************************************************
add document part (inline text, paragraph or picture) to FContent array
*************************************************************************)
procedure TDocument.Add(Style: PStyle;const Text: ANSIString;Index: integer);
var NewItem: PDocPart;
begin
 if (FCount >= (FCapacity-1)) then AllocateNew;
 New(NewItem);
 NewItem^.Index:=Index;
 case Style^.SType of
  stBlock, stInline:
   begin
     NewItem.PType:=ptText;
     NewItem^.FontSize:=Style^.Size;
     NewItem^.Color:=Style^.Color;
     NewItem^.Text:=FormatText(Text);
   end;
  stPicture:
   begin
     AddBreak;
     NewItem^.PType:=ptPicture;
     NewItem^.Image:=OpenPicture(Text);
   end;
  stLink: Error('???');
 end;{case}
 FContent^[FCount]:=NewItem;
 Inc(FCount);
end;

(*******************************************************************************
this is case sensitive replacement of Styles.IndexOf
*******************************************************************************)
function TDocument.IndexOfStyle(const S: ShortString):integer;
var I: integer;
begin
 RESULT:=-1;
 for I:=0 to (Styles.Count-1) do
  if (s = Styles[I]) then begin
   RESULT:=I;
   BREAK;
  end;{if}
end;

(****************************************************************************
recursive parser for sml documents
***********************************************************************)
function TDocument.Process(ParentStyle: PStyle;const SelfTag: ANSIString): ANSIString;
var T1: ANSIString;
    EndTag: boolean;
    I: integer;
    S, S1: PStyle;
begin
 EndTag:=false;
 RESULT:='';

 New(S);       // create new copy of PStyle
 Move(ParentStyle^, S^, SizeOf(TStyle)); // fill with parent style
 I:=IndexOfStyle(SelfTag);// case sensitive check
 if (I = -1) then Error('Undefined style "'+SelfTag+'"');
 S1:=PStyle(Styles.Objects[I]);
 S.SType:=s1.SType;        // replace inherited properties with self
 if (S1.Color <> clNone) then S.Color:=s1.Color;
 if (S1.Size <> 0) then S.Size:=S1.Size;

 I:=LoaderMaxI;Inc(LoaderMaxI);

 if (S.SType=stBlock) then AddBreak;

 if (S.SType = stLink) then begin  // Link
  Result:=GetLink(ReadText(true));
  if (ReadTag(true) <> '/'+SelfTag) then Error('Invalid Link');
 end{if}

 else
 repeat
  if CheckTag then begin   // Tag
   T1:=ReadTag(true);
   if (T1 = '/'+SelfTag) then EndTag:=true
   else begin
    T1:=Self.Process(S, T1);
    if (T1 <> '') then Links.AddObject(T1, TObject(I));
   end{else}
  end{if}
  else begin              // Text
    T1:=ReadText(true);
    Add(S, T1, I);
  end;{else}
 until EndTag;
 if (S.SType in [stBlock, stPicture]) then AddBreak;
 Dispose(S);
end;

(***************************************************************************
do some finalization
**********************************************************************)
procedure TDocument.CreateLinksAndLines;
var I, J, K, L: integer;
begin
 for I:=0 to (Links.Count-1) do begin   // assign links
  K:=integer(Links.Objects[I]);
  for J:=0 to (FCount-1) do
   if ((FContent^[J] <> ptrBreak) and (FContent^[J]^.Index = K)) then
     FContent^[J]^.Link:=Links[I];
 end;{for}

 L:=0;J:=0;
 for I:=0 to (FCount-1) do begin	// format Content for DisplayThread
  if (FContent^[I] = ptrBreak) then Inc(L) // remove nil items
   else begin
    FContent^[I]^.Index:=L; // Write Line number into Index variable
    FContent[J]:=FContent[I];
    Inc(J);
   end;{else}
 end;{for}
 if (FCount > 0) then begin // add nil mark if not empty document
  FContent[J]:=nil;
  FCount:=J;
 end;
end;

(******************************************************************************
constructor which tryes to load the document (and also style file)
**************************************************************************)
constructor TDocument.OpenFile(const FileName: ANSIString);
var Path: ANSIString;
    STYLE: ShortString;
    I: integer;
    S: PStyle;
begin
 inherited OpenFile(FileName);

 STYLE:=ReadTag(true);         // open style file
 Path:=AddBSlash(ConfigInfo.StylePath)+STYLE+'.sty';
 if FileExists(Path) then Styles:=LoadStyles(Path)
 else begin
  Path:=AddBSlash(ExtractFilePath(ReplaceChar(FileName,'/','\')))+STYLE+'.sty';
  if FileExists(Path) then Styles:=LoadStyles(Path)
   else raise Exception.Create('Style file not found');
 end;{else}

 I:=IndexOfStyle(STYLE);            // create main style
 if (I = -1) then Error('Style "'+STYLE+'" not found');
 New(S);
 Move(PStyle(Styles.Objects[I])^,S^, SizeOf(TStyle));
 if (S.Color = clNone) then S.Color:=clBlack;
 if (S.Size = 0) then S.Size:=ConfigInfo.DefaultFontHeight;
 LoaderMaxI:=0;
 Links:=TStringList.Create;

 Process(S, Style); // load document by recursive calling of Process

 CreateLinksAndLines; // do some formatting

 Links.Free;	// release memory
 Dispose(S);
 for I:=0 to (Styles.Count-1) do Dispose(PStyle(Styles.Objects[I]));
 Styles.Free;
end;



end.

