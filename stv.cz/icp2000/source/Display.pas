{$I hdr.inc}
unit Display;

interface

uses Classes, Windows, Graphics, Forms, docunit;

type
 ///////////////////////////////////////////////////////////
 // Structures for font management
 TFontHandle = record           // - fonts are created only when document is being loaded
                Handle: HFONT;
                case boolean of
                true:  (size: byte;ul: bytebool); // ul = Underline
                false: (attr: word);
 	       end;
 PFonts = ^TFonts;
 TFonts = array[0..255] of TFontHandle;

 ///////////////////////////////////////////////////////////////
 // structure that keeps position of word in document
 TWordPos = record	// it's used for writing text - keeps position of last/first word in line
                Part:	integer;
 	     	WordNum:integer;
            end;

  ///////////////////////////////////////////////////////////
  // heights of each paragraph in document
  PIntArray = ^TIntArray; //it's recalculated when width of form has changed
  TIntArray = array[0..MaxInt div 16] of integer;


  TDisplayThread = class(TThread)
   protected
    procedure   Execute;override;
   private
    OutputForm:	TForm;
    TopY:	integer;
    DocH: 	integer; // total height of document (sum of items in Lines)
    Canvas:	record
    		DC:	HDC;
    		Image:	HBitmap;
                Width: 	integer;
                Height:	integer;
                B:	HBRUSH;
                Fonts:	PFonts;
                FontCount: integer;
                DefaultFont: HFont;
                end;
    ImportImg:	record
    		Pic: 	TBitmap;
                Y, H, W:integer;
                Link:	ShortString;
                end;
    Paras:      PIntArray;// height of lines
    LineCount:  integer;
    procedure   Draw(_NewW: boolean); // paints canvas
{S} procedure   PaintPicture; 	// paints image in document on canvas
{S} procedure   GetPictureSize; // get image size using ImportImg
{S} procedure   SetScrollBar;
{S} procedure   CopyOutput;

    procedure   PaintPara(_NewW: boolean;_Y, _LineI: integer);
    procedure   TextHeight(const _SWord: TWordPos;var _EWord: TWordPos;var _Height: integer);
    procedure   PaintTextLine(const _SWord, _EWord: TWordPos;BottomY: integer);
    procedure   GetFont(Size: byte;Underline: boolean);
    procedure   ClearFonts;
   public
    constructor Create(Form: TForm);
  end;

var
 TCtrl: record	   // this record is used for controling all thread operations
         NewFont:       boolean;
  	 Accessible:    boolean;
         Stopped:       boolean; // thread won't try to access Document
         DoPaint:       boolean;
         DoRepaint:     boolean;
         Width,Height:  integer;
         Top,Left:      integer;
         YPos:          integer;
         Content:       PDocParts;
         ContentChanged:boolean;
         Thread:        TThread;
         Links0, Links: TStringList;
 	end;


// set TCtrl.Accessible to false  and waits for response in TCtrl.Stopped
procedure PauseThread;

// enables execution of TDisplayThread
procedure UnpauseThread;

// Sets new font style
procedure SetDocumentFont;

implementation

uses MainUnit, SysUtils, config;

{$I Display.INC}

{ TDisplayThread }

(*************************************************************************
create thread - create DC, set text alignment and so on...
**************************************************************************)
constructor TDisplayThread.Create(Form: TForm);
begin
 inherited Create(false);
 OutputForm:=Form;
 Canvas.DC:=CreateCompatibleDC(OutputForm.Canvas.Handle);
 SetBkMode(Canvas.DC, TRANSPARENT);
 SetTextAlign(Canvas.DC, TA_LEFT or TA_BOTTOM);
 SetDocumentFont;
 Canvas.DefaultFont:=GetCurrentObject(Canvas.DC,OBJ_FONT);
 FreeOnTerminate:=true;
 Priority:=ConfigInfo.Priority;
end;

(************************************************************************
main thread's method
************************************************************************)
procedure TDisplayThread.Execute;
var B1,B2: boolean;
    I: integer;
begin
 repeat
  if (not TCtrl.Accessible) then begin // is Content accessible ?
     TCtrl.Stopped:=true;       // No, probably loading new document
//   Sleep(0);
  end {if}

  else begin			// Yes,
   TCtrl.Stopped:=false;
   B1:=(Canvas.Width <> TCtrl.Width);
   B2:=(Canvas.Height <> TCtrl.Height) or B1;
   if TCtrl.ContentChanged then begin
    I:=0;                 // new document has been loaded
    TCtrl.ContentChanged:=false;
    while (TCtrl.Content^[I] <> nil) do Inc(I);
    I:=TCtrl.Content^[I-1]^.Index;
    ReallocMem(Paras,(I+1) * SizeOf(integer));
    LineCount:=I+1;
    DocH:=0;
    B1:=true;
   end;

   if (B1 or B2) then begin // repainting is required
    Canvas.Width:=TCtrl.Width;
    Canvas.Height:=TCtrl.Height;
    TopY:=TCtrl.YPos;
    if B2 then begin  // main form has been resized
      Canvas.Image:=CreateCompatibleBitmap(OutputForm.Canvas.Handle,Canvas.Width,Canvas.Height);
      DeleteObject(SelectObject(Canvas.DC, Canvas.Image));
    end;
    Draw(B1);
   end{if}
   else
    if (TopY <> TCtrl.YPos) or TCtrl.DoRepaint then begin
     TopY:=TCtrl.YPos;
     Draw(false);
    end;{if}
  end;// if Accessible

  if TCtrl.DoPaint then Synchronize(CopyOutput);
        // ^^^ DoPaint is set by MainForm.OnPaint event...
        // ...and must be performed whenever any document is loaded
 until Terminated;
end;

(****************************************************************************
copies canvas image on the mainform
and creates copy of links list for main thread
*****************************************************************************)
procedure TDisplayThread.CopyOutput;
var I: integer;
    P: PRect;
begin
         /// copy links
  for I:=0 to (TCtrl.Links.Count-1) do Dispose(PRect(TCtrl.Links.Objects[I]));
  TCtrl.Links.Clear;
  TCtrl.Links.Capacity:=TCtrl.Links0.Count+1;
  for I:=0 to (TCtrl.Links0.Count-1) do begin
    New(P);
    Move(PRect(TCtrl.Links0.Objects[I])^, P^, SizeOf(TRect));
    TCtrl.Links.AddObject(TCtrl.Links0[I],TObject(P));
  end;{for}
        /// copy canvas
 BitBlt(OutputForm.Canvas.Handle, TCtrl.Left, TCtrl.Top, Canvas.Width, Canvas.Height, Canvas.DC, 0, 0, SRCCOPY);
 TCtrl.DoPaint:=false;  // clear request
end;

(**********************************************************************
this method provides thread's feedback - controls scrollbar
***********************************************************************)
procedure TDisplayThread.SetScrollBar;
var I: integer;
begin
 I:=DocH-Canvas.Height+1;
 if (I < 0) then I:=0;
 with TMainForm(OutputForm).ScrollBar1 do begin
  Max:=I;
  Enabled:=(I > 0);
 end;{with}
end;

(***************************************************************************
returns image size using ImportImg record
****************************************************************************)
procedure TDisplayThread.GetPictureSize;
begin
 ImportImg.H:=ImportImg.Pic.Height;
 ImportImg.W:=ImportImg.Pic.Width;
end;

(***************************************************************************
returns image size using ImportImg record
and also paints the image on canvas and adds link
****************************************************************************)
procedure TDisplayThread.PaintPicture;
var
 B: TBitmap;
 P: PRect;
begin
 B:=ImportImg.Pic;
 ImportImg.H:=B.Height;
 ImportImg.W:=B.Width;
 New(P);
 P^:=Bounds((Canvas.Width-ImportImg.W) shr 1, ImportImg.Y,
 		ImportImg.W, ImportImg.H);
 BitBlt(Canvas.DC,		// destination DC
 	P^.Left,P^.Top,		// TopLeft
        B.Width, ImportImg.H,	// image Width,  Height
        B.Canvas.Handle,	// source DC
        0, 0,			// Source TopLeft
        SRCCOPY);		// raster operation
 if (ImportImg.Link <> '') then
  TCtrl.Links0.AddObject(ImportImg.Link, TObject(P))
 else Dispose(P);
end;

(*****************************************************************************
this method calls PaitPara for every visible paragraph in document
(when form is resized then for all paragraphs)
***********************************************************************)
procedure TDisplayThread.Draw(_NewW: boolean);
var I, Ly, tH, start: integer;
begin
 TCtrl.Links0.Clear;
 TCtrl.DoRepaint:=false;
 Ly:=0;			// Y pos. of current line in document

 Canvas.B:=CreateSolidBrush(ConfigInfo.BGColor);  // clear canvas
 DeleteObject(SelectObject(Canvas.DC, Canvas.B));
 FillRect(Canvas.DC, Rect(0,0,Canvas.Width,Canvas.Height), Canvas.B);

 start:=0;
 if (not _NewW) then begin  // find first visible line
  repeat
  if (Ly + Paras^[start]) < TopY then begin
   Inc(Ly,Paras^[start]);
   Inc(start);
  end;
  until ((Ly + Paras^[start]) >= TopY);
  if start < 0 then start:=0;
 end;

 for I:=start to (LineCount-1) do begin
   if (not _NewW) and (Ly > (TopY+Canvas.Height)) then BREAK;
   PaintPara(_NewW, Ly-TopY, I);
   Inc(Ly, Paras^[I]);
   if (not TCtrl.Accessible) then EXIT;
  end;{for}

 if _NewW then begin  // if New width then calculate total height
  tH:=0;
  for I:=0 to (LineCount-1) do Inc(tH, Paras^[I]);
  DocH:=tH;
  synchronize(SetScrollBar);
 end;{if}

 synchronize(CopyOutput);

end;

(*******************************************************************************
 calculates the paragraph height and paints the paicture or text if required
******************************************************************************)
procedure TDisplayThread.PaintPara(_NewW: boolean;_Y, _LineI: integer);
var I: integer;
    P: PDocPart;
    tH:integer;	     // total height
    MaxH: integer;   // max height of one displayed line
    firstW: TWordPos;// first
    lword: TWordPos; // last
begin
 I:=-1;
 repeat // find first element
  Inc(I);
  P:=TCtrl.Content^[I];
  if (P = nil) then EXIT;
 until (P^.Index = _LineI);

 if (P^.PType = ptPicture) then begin 	// *** image
   ImportImg.Pic:=P^.Image;
   ImportImg.Y:=_Y;
   ImportImg.Link:=P^.Link;
   if (_Y < Canvas.Height) then Synchronize(PaintPicture)
    else Synchronize(GetPictureSize);
   if _NewW then begin
    tH:=ImportImg.H;
    Paras^[_LineI]:=tH;
   end;
  end{if}
  else begin			// *********** TEXT
   lword.Part:=I;
   lword.WordNum:=0;
   tH:=0;
   repeat
    firstW:=lword;
    MaxH:=0;
    TextHeight(firstW, lword, MaxH);
    Inc(_Y, MaxH);Inc(tH, MaxH);
    if ((_Y-MaxH) > Canvas.Height) then begin // if below the view
     if (not _NewW) then EXIT   // result required ?
    end
    else                                // VVV we're not below view
     if (_Y > 0) then PaintTextLine(firstw, lword, _Y);
    P:=TCtrl.Content^[lword.part];
   until (P = nil) or (P^.Index > _LineI);
   Paras^[_LineI]:=tH;
  end;{else}
end;

///////////////////////////////////////////////////////////////////
//////////////     Fonts            ////////////////////////////////

(**********************************************************************
sets new current font for canvas's DC
**********************************************************************)
procedure TDisplayThread.GetFont(Size: byte;Underline: boolean);
var I: integer;
    F: ^TFontHandle;
    FAttr: word;
begin
 if TCtrl.NewFont then ClearFonts // new font have to be created
 else begin
  FAttr:=Size;                    // look for already created font
  if UnderLine then Inc(FAttr,256);
  for I:=0 to (Canvas.FontCount-1) do begin
   F:=@canvas.Fonts^[I];
   if (F^.Attr = FAttr) then begin
    SelectObject(Canvas.DC,F^.Handle);
    EXIT;
   end;{if}
  end;{for}
 end;{else}
 ReallocMem(Canvas.Fonts, SizeOf(TFontHandle) * (Canvas.FontCount+2));
 F:=@canvas.Fonts^[Canvas.FontCount];
 F^.size:=Size;
 F^.ul:=Underline;
 Inc(Canvas.FontCount);
 DisplayLogFont.lfHeight:=-MulDiv(F^.Size, GetDeviceCaps(Canvas.DC, LOGPIXELSY), 72);
 if Underline then DisplayLogFont.lfUnderline:=1 else DisplayLogFont.lfUnderline:=0;
 F^.Handle:=CreateFontIndirect(DisplayLogFont);
 SelectObject(Canvas.DC,F^.Handle);
end;

(************************************************************************
font properties have been changed and all font handles must be destroyed
************************************************************************)
procedure TDisplayThread.ClearFonts;
var I: integer;
begin
 SelectObject(Canvas.DC, Canvas.DefaultFont);
 for I:=0 to (Canvas.FontCount-1) do
  DeleteObject(Canvas.Fonts^[I].Handle);
 ReallocMem(Canvas.Fonts,0);
 Canvas.FontCount:=0;
 TCtrl.NewFont:=false;
end;

////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////

(***************************************************************************
this procedure writes text begining with _SWord
and ending before _EWord on line with bottom y-position = BottomY
and also creates link rectangles
****************************************************************************)
procedure TDisplayThread.PaintTextLine(const _SWord, _EWord: TWordPos;BottomY: integer);
var I, X: integer;
    P: PDocPart;
    S: ANSIstring;
    R: PRect;
    size: TSize;
begin
 X:=0;            // X position
 I:=_SWord.Part;
 P:=TCtrl.Content^[I];
 if (_SWord.Part = _EWord.Part) then S:=GetWords(P^.Text,_SWord.WordNum, _EWord.WordNum-_SWord.WordNum)
  else
  if (_SWord.WordNum > 0) then S:=GetWords(P^.Text,_SWord.WordNum, 0)
   else S:=P^.Text;
 repeat
  if (P^.Link <> '') then begin
   New(R);
   TCtrl.Links0.AddObject(P^.Link, TObject(R));
  end{if}
  else R:=nil;

  if S[Length(S)] = ' ' then SetLength(S, Length(S)-1);
  GetFont(P^.FontSize,P^.Link <> '');
  GetTextExtentPoint32(Canvas.DC, PChar(S), Length(S), Size);
  if (R <> nil) then R^:=Bounds(X, BottomY-Size.cy, Size.cx, Size.cy);
  SetTextColor(Canvas.DC, P^.Color);
  TextOutA(Canvas.DC, X, BottomY, PChar(S), Length(S));
  Inc(X, Size.cx);
  GetTextExtentPoint32(Canvas.DC, ' ',1, Size); // add space
  Inc(X, Size.cx);

  Inc(I);
  P:=TCtrl.Content^[I];
  if (I < _EWord.Part) then S:=P^.Text
  else
   if (I = _EWord.Part) then
    if (_EWord.WordNum = 0) then BREAK
     else S:=GetWords(P^.Text, 0, _EWord.WordNum);
 until (I > _EWord.Part);
end;

(*******************************************************************************
//// the most complicated and probably the most important method ///////////////
// this procedure returns height of line and the last word on this line ////////
*******************************************************************************)
procedure TDisplayThread.TextHeight(const _SWord: TWordPos;var _EWord: TWordPos;var _Height: integer);
var I: integer;
    P: PDocPart;
    S: ANSIString;
    Size: TSize;
    rWidth: integer;
    maxWords: integer;
    lindex: integer;
    firstword,PartI: integer;
    spWidth: integer;      // space width
    lastfit: integer;
begin
 rWidth:=Canvas.Width-5;   // remaining space on line
 PartI:=_SWord.Part;
 P:=TCtrl.Content^[PartI];
 lindex:=P^.Index;
 firstword:=_SWord.WordNum;
 repeat
  GetFont(P^.FontSize, P^.Link <> '');          // get font
  GetTextExtentPoint32(Canvas.DC, ' ',1, Size);// get space width
  spWidth:=Size.cx;
  _EWord.Part:=PartI;
  _EWord.WordNum:=firstword;
  maxWords:=WordCount(P^.Text)-firstword;
  I:=0;
  lastfit:=0;
  repeat                   // find out how many words can fit in line
    S:=GetWords(P^.Text, firstword+I, 1);
    GetTextExtentPoint32(Canvas.DC, PChar(S), Length(S), Size);
    Inc(I);
    if (rWidth >= Size.cx) then lastfit:=I;
    Dec(rWidth, Size.cx+spWidth);
  until (I = maxWords) or (rWidth <= 0);

  if (lastfit = 0) then begin// first word is longer then remaining space
    if (_SWord.Part = PartI) then begin // if it is first word on line
     if (_Height < Size.cy) then _Height:=Size.cy;
     if (maxWords > 1) then _EWord.WordNum:=firstword+1
      else begin _EWord.WordNum:=0;_EWord.Part:=PartI+1;end;
    end;{if}
    EXIT;
  end;

  if (_Height < Size.cy) then _Height:=Size.cy;

  if (lastfit < maxWords) then begin    // current part is last-> return word number
    _EWord.WordNum:=firstword+lastfit;
    EXIT;
  end;

  Inc(PartI);         // next docpart
  firstword:=0;

  P:=TCtrl.Content^[PartI];
 until (P = nil) or (P^.Index > lindex);
 _EWord.WordNum:=0;_EWord.Part:=PartI;
end;


end.

