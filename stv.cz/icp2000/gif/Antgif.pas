{******************************************************************************}
{**                                                                          **}
{**  GIF file routines. I've used this unit many times but now I prefere to  **}
{**  use GIF routines from RX Library (http://www2.crosswinds.net/~rxlib/)   **}
{**                                                                          **}
{**  Author:    KARPOLAN                                                     **}
{**  E-Mail:    karpolan@yahoo.com , karpolan@utilmind.com                   **}
{**  Home Page: http://karpolan.i.am, http://www.utilmind.com                **}
{**  Copyright © 1996-99 by KARPOLAN.                                        **}
{**  Copyright © 1999, UtilMind Solutions.                                   **}
{**                                                                          **}
{******************************************************************************}
{**  History:                                                                **}
{**                                                                          **}
{**  31 aug 1999 - Last modified... Prepared for public release.             **}
{******************************************************************************}
Unit AntGif;

{$Include AntUnits.Inc}

{*******************************************************************************
     The GIF handling code is based heavily on routines written for Borland
   Pascal 7.0 by Sean Wenzel, CIS 71736,1245.
     Thanks to High Gear, Inc. for examples and High Gear VCL
*******************************************************************************}

{*******************************************************************************
   Install this file like component and standart TPicture properties will
   understand GIF format. You can use standart TImage component for GIFs
*******************************************************************************}

{$A-}  {** Not Aligned Packed Records **}
{$LongStrings ON}
Interface

Uses
  Windows, Math, SysUtils, Classes, Graphics;

Const
  gifMaxScreenWidth        = 2048;
  gifMaxCodes              = 4095;
  strGifHeaderSignature    = 'GIF';
  bmpFileSignature         = $4d42;

Type
  TGifFileHeader = Packed Record
    Signature : Array[0..2] of Char; {** Header Signature - 'GIF' **}
    Version   : Array[0..2] of Char; {** Gif Format Version : '87a' or '89a' **}
  End;{TGifFileHeader = Packed Record}

  TGifDataSubBlock = Packed Record
    Size : Byte;                  {** Block's Size **}
    Data : Array[1..255] of Byte; {** Data Block   **}
  End;{TGifDataSubBlock = Packed Record}

  TGifLogicalScreenDescriptor = Packed Record
    ScreenWidth          : Word;   { logical screen width in pixels }
    ScreenHeight         : Word;   { logical screen height in pixels }
    PackedFields         : Byte;   { screen and color map info - see below }
    BackGroundColorIndex : Byte;   { index to global color table }
    AspectRatio          : Byte;   { pixel aspect ration : actual ratio = (AspectRatio + 15) / 64 }
  End;{TGifLogicalScreenDescriptor = Packed Record}

  TGifImageDescriptor = Packed Record
    Separator    : Byte;  { Image Descriptor identifier - always $2C }
    ImageLeftPos : Word;  { X position of image on the logical screen }
    ImageTopPos  : Word;  { Y position of image on the logical screen }
    ImageWidth   : Word;  { width of image in pixels }
    ImageHeight  : Word;  { height of image in pixels }
    PackedFields : Byte;  { Image and color table data information }
  End;{TGifImageDescriptor = Packed Record}

{** One Item Of Color Table }
  TGifColorItem = Packed Record
    Red    : Byte;  { Red color element }
    Green  : Byte;  { Green color element }
    Blue   : Byte;  { Blue color element }
  End;{TGifColorItem = Packed Record}

{** Color Table }
  TGifColorTable = Array[0..255] of TGifColorItem;

{** One Line In Decoded Image **}
  TGifLineData = Array[0..gifMaxScreenWidth] of Byte;

{##############################################################################}
{## New Class Of TGraphic For Holding GIFs ####################################}
{##############################################################################}
  EGif = Class(Exception);

  TGif = Class(TGraphic)
  Private
    fGifStream        : TMemoryStream;    { file stream for the Gif file }
    fBitmap           : TBitmap;
    fBitmapStream     : TMemoryStream;
    fBitmapLineList   : TList;            { Holds TBitmapLine objects }
    fFileName         : TFileName;
    fBitmapInfoHeader : TBitmapInfoHeader;{ File Header for bitmap file }
    Header            : TGifFileHeader;   { Gif file header }
    LogicalScreen     : TGifLogicalScreenDescriptor; { Gif screen descriptor }
    ImageDescriptor   : TGifImageDescriptor;         { Gif  image descriptor }
    GlobalColorTable  : TGifColorTable;
    LocalColorTable   : TGifColorTable;
    UseLocalColors    : Boolean;          { True if local colors in use }
    Interlaced        : Boolean;          { True if image is Interlaced }
    LZWCodeSize       : Byte;             { Minimum size of the LZW codes in bits }
    ImageData         : TGifDataSubBlock; { Variable to store Incoming Data }
    TableSize         : Word;             { Number of entrys in the color table }
    BitsLeft          : SmallInt;         { bits left in byte }
    BytesLeft         : SmallInt;         { bytes left in block }
    CurrCodeSize      : SmallInt;         { Current size of code in bits }
    ClearCode         : SmallInt;
    EndingCode        : SmallInt;
    Slot              : Word;             { Position that the next new code is to be added }
    TopSlot           : Word;             { Highest slot position for the current code size }
    HighCode          : Word;             { highest code that does not require Decoding }
    NextByte          : SmallInt;         { Index to the next byte in the datablock Array }
    CurrByte          : Byte;             { the current byte }
    LineBuffer        : TGifLineData;        { Array for buffer line output }
    CurrentX          : SmallInt;         { Current screen X location }
    CurrentY          : SmallInt;         { Current screen X location }
    InterlacePass     : Byte;             { interlace pass number }
  {** Stack for the Decoded codes **}
    DecodeStack       : Array[0..gifMaxCodes] of Byte;
  {** Prefixes/Suffixes Routine **}
    Prefix            : Array[0..gifMaxCodes] of SmallInt;
    Suffix            : Array[0..gifMaxCodes] of SmallInt;
  {** Streams Routine **}
    Procedure InitCompressionStream;
    Procedure ReadSubBlock;
    Procedure WriteStream(Stream    : TStream;
                          WriteSize : Boolean);
    Procedure ReadStream(Size   : LongInt;
                         Stream : TStream);
  {** Decode Routine **}
    Procedure DecodeGifHeader;
    Procedure DecodeGif;
  {** Convert Routine **}
    Procedure ConvertGif;
    Procedure ConvertGifToBmp;
  {** Process Routine **}
    Procedure CheckObjects;
    Procedure DrawGifLine;
    Function ProcessExtensions : Boolean;
    Function NextCode : Word;
  Protected
  {** Override This **}
    Procedure Draw(ACanvas    : TCanvas;
                   Const Rect : TRect);                                Override;
  {** Properties Overrides **}
    Function  GetEmpty : Boolean;                                      Override;
    Function  GetHeight   : integer;                                   Override;
    Procedure SetHeight(A : integer);                                  Override;
    Function  GetWidth    : integer;                                   Override;
    Procedure SetWidth (A : integer);                                  Override;
  {** Streams Routine **}
    Procedure ReadData (Stream : TStream);                             Override;
    Procedure WriteData(Stream : TStream);                             Override;
  Public
  {** Constr/Destr**}
		Constructor Create;                                                Override;
		Destructor  Destroy;                                               Override;
  {** Override This **}
    Procedure Assign(Source : TPersistent);                            Override;
  {** Files Routine **}
    Procedure LoadFromFile(Const FileName : String);                   Override;
    Procedure SaveToFile  (Const FileName : String);                   Override;
  {** Streams Routine **}
    Procedure LoadFromStream(Stream : TStream);                        Override;
    Procedure SaveToStream  (Stream : TStream);                        Override;
  {** ClipBoard Routine **}
    Procedure LoadFromClipBoardFormat(AFormat  : Word;
                                      AData    : THandle;
                                      APalette : HPalette);            Override;
    Procedure SaveToClipBoardFormat(Var AFormat  : Word;
                                    Var AData    : THandle;
                                    Var APalette : HPalette);          Override;
  {** Properties Routine **}
    Property GifStream   : TMemoryStream
      Read   fGifStream
      Write  fGifStream;
    Property Bitmap      : TBitmap
      Read   fBitmap
      Write  fBitmap;
    Property FileName    : TFileName
      Read fFileName;
  {** Old Properties **}
    Property Empty;
    Property Height;
    Property Modified;
    Property Width;
    Property OnChange;
  End;{TGif = Class(TGraphic)}

Procedure Register;

{##############################################################################}
{******************************************************************************}
{##############################################################################}
Implementation
{##############################################################################}
{******************************************************************************}
{##############################################################################}

Procedure Register;
Begin
  RegisterClass(TGif);
//  TPicture.RegisterFileFormat('GIF', 'GIF Files', TGif);
End;{Procedure Register}


Const
{** Error Messages Constants **}
  strNoFile             = 'Gif File Not Found';
  strNotGifFile         = 'File isn''t a Gif File';
  strNoGlobalColorTable = 'Global Color Table Not Found';
  strPreceded           = 'Image Descriptor Preceded';
  strEmptyBlock         = 'Data Block is Empty';
  strWrongCodeSize      = 'Wrong Gif Code Size';
  strWrongCode          = 'Wrong Gif Code';
  strWrongBitSize       = 'Wrong Bit Size';

{** Terminator For Data Blocks **}
{  BlockTerminator : Byte = 0;

{** Logical Screen Descriptor Field Masks **}
  lsdGlobalColorTable = $80;  { set if global color table follows L.S.D. }
  lsdColorResolution  = $70;  { Color resolution - 3 bits }
  lsdSort             = $08;  { set if global color table is sorted - 1 bit }
  lsdColorTableSize   = $07;  { size of global color table - 3 bits }
														  { Actual size = 2^value+1    - value is 3 bits }
{** Separator For Image Blocks **}
  ImageSeparator : Byte = $2C;

{** Image Descriptor Bit Masks **}
  idLocalColorTable   = $80;  { set if a local color table follows }
  idInterlaced        = $40;  { set if image is Interlaced }
  idSort              = $20;  { set if color table is sorted }
  idReserved          = $0C;  { reserved - must be set to $00 }
  idColorTableSize    = $07;  { size of color table as above }

{** Indicates End of Gif Data Stream **}
{	Trailer : Byte = $3B;

{** Gif89a Standard Introduced Control Extensions **}
  ceExtensionIntroducer            = $21;
  ceGraphicControlLabel            = $F9;
  ceGraphicControlBlockSize        = $04;
  cePlainTextLabel                 = $01;
  cePlainTextBlockSize             = $0C;
  ceApplicationExtensionLabel      = $FF;
  ceApplicationExtensionBlockSize  = $0B;
  ceCommentLabel                   = $FE;

{** Bit Masks for Use With Next Code **}
  CodeMask : Array[0..12] of SmallInt = (
    0,
    $0001, $0003,
    $0007, $000F,
    $001F, $003F,
    $007F, $00FF,
    $01FF, $03FF,
    $07FF, $0FFF);

Type
{** Holds Single Line of Bitmap Image **}
  TBitmapLine = Class(TObject)
    BitmapLine : TGifLineData;
    LineNumber : SmallInt;
  End;{TBitmapLine = Class(TObject)}

  TGifExtensionBlock = Packed Record
    Introducer     : Byte;   {** Fixed value of ExtensionIntroducer **}
    ExtensionLabel : Byte;
  End;{TGifExtensionBlock = Packed Record}

  TGifGraphicsControlExtension = Packed Record
    BlockSize    : Byte;  { Size of remaining fields. Always $04 }
    PackedFields : Byte;  { Method of graphics disposal to use }
    DelayTime    : Word;  { Hundredths of seconds to wait }
    ColorIndex   : Byte;  { Transparent color index }
    Terminator   : Byte;  { Block terminator. Always 0 }
  End;{TGifGraphicsControlExtension = Packed Record}

  TGifPlainTextExtension = Packed Record
    BlockSize        : Byte;   { Size of extension block. Always $0C }
    TextGridLeft     : Byte;   { X position of text grid in pixels }
    TextGridTop      : Byte;   { Y position of text grid in pixels }
    TextGridWidth    : Byte;   { Width of the text grid in pixels }
    TextGridHeight   : Byte;   { Height of the text grid in pixels }
    CellWidth        : Byte;   { Width of a grid cell in pixels }
    CellHeight       : Byte;   { Height of a grid cell in pixels }
    TextFgColorIndex : Byte;   { Text foreground color index value }
    TextBgColorIndex : Byte;   { Text background color index value }
  End;{TGifPlainTextExtension = Packed Record}

{** The next thing in a plain text extension is one or more data sub-blocks
    containing the actual textual information that is to be rendered as a
    graphic. Use the TGifDataSubBlock Type. The appearance of the
    BlockTerminator (0) marks the end of the Plain Text Extension block. **}
  TGifApplicationExtension = Packed Record
    BlockSize   : Byte;                 { Size of extension block. Always $0B }
    Identifier  : Array[1..8] of Char;  { Application Identifier }
    AuthentCode : Array[1..3] of Byte;  { Application authentication code }
  End;{TGifApplicationExtension = Packed Record}


{##############################################################################}
{## TGif = Class(TGraphic) ####################################################}
{##############################################################################}

{***********************}
{** Sort List Routine **}
{***********************}
Function SortBitmapLineList(Item1, Item2 : Pointer) : integer;
Var
  Line1, Line2 : TBitmapLine;
Begin
  try
  {** Pointers To Typed Pointers **}
    Line1 := Item1;
    Line2 := Item2;
  {** Sort Result **}
    Result := Line1.LineNumber - Line2.LineNumber;
  except
    Result := 0;
  end;{try .. except}
End;{Function SortBitmapLineList}


{******************************************************************************}
{** Public ********************************************************************}
{******************************************************************************}
{** Init/Done **}
{***************}
Constructor TGif.Create;
Begin
  Inherited Create;
  fBitmapLineList := TList        .Create;
  fBitmapStream   := TMemoryStream.Create;
  fGifStream      := TMemoryStream.Create;
  fBitmap         := TBitmap      .Create;
End;{Constructor TGif.Create}

Destructor TGif.Destroy;
Begin
  fBitmap      .Free;
  fGifStream   .Free;
  fBitmapStream.Free;
{** frees all of the bitmap line objects, then clears the list **}
  if Assigned(fBitmapLineList) then
   begin
     fBitmapLineList.Clear;
     fBitmapLineList.Free;
   end;{if Assigned(fBitmapLineList) then}
  Inherited Destroy;
End;{Destructor TGif.Destroy}


{*******************}
{** Override This **}
{*******************}
Procedure TGif.Assign(Source : TPersistent);
Begin
  if (Source is TGif) then
   begin
     CheckObjects;
     fGifStream.Clear;
     (Source as TGif).GifStream.Seek(0, soFromBeginning);
     fGifStream.LoadFromStream((Source as TGif).GifStream);
     ConvertGif;
     Changed(Self);
   end
  else Inherited Assign(Source);
End;{Procedure TGif.Assign}


{*******************}
{** Files Routine **}
{*******************}
Procedure TGif.LoadFromFile(Const FileName : String);
Begin
{** For New File **}
  if fFileName = FileName
   then Exit;
{** Check File Existing **}
  if not FileExists(FileName)
   then Raise EGif.Create(strNoFile);
{** Check File Extention **}
  if (UpperCase(ExtractFileExt(FileName)) <> '.GIF')
   then Raise EGif.Create(strNotGifFile);
{** Load From File**}
  fFileName := FileName;
  fGifStream.LoadFromFile(fFileName);
  ConvertGif;
End;{Procedure TGif.LoadFromFile}

Procedure TGif.SaveToFile(Const FileName: String);
Begin
  fGifStream.SaveToFile(FileName);
End;{Procedure TGif.SaveToFile}


{********************}
{** Stream Routine **}
{********************}
Procedure TGif.LoadFromStream(Stream : TStream);
Begin
{** Check For Stream **}
  if not Assigned(Stream)
   then Exit;
{** Loading **}
  fGifStream.LoadFromStream(Stream);
  ConvertGif;
  Changed(Self);
End;{Procedure TGif.LoadFromStream}

Procedure TGif.SaveToStream(Stream : TStream);
Begin
  WriteStream(Stream, False);
End;{Procedure TGif.SaveToStream}


{***********************}
{** ClipBoard Routine **}
{***********************}
Procedure TGif.LoadFromClipBoardFormat(AFormat  : Word;
                                       AData    : THandle;
                                       APalette : HPalette);
Begin
End;{Procedure TGif.LoadFromClipBoardFormat}

Procedure TGif.SaveToClipBoardFormat(Var AFormat  : Word;
                                     Var AData    : THandle;
                                     Var APalette : HPalette);
Begin
End;{Procedure TGif.SaveToClipBoardFormat}

{******************************************************************************}
{** Protected *****************************************************************}
{******************************************************************************}
{** Override This **}
{*******************}
Procedure TGif.Draw(ACanvas    : TCanvas;
                    Const Rect : TRect);
Var
  destDC                : HDC;
  destX, destY,
  destWidth, destHeight : SmallInt;
  srcDC                 : HDC;
  srcX, srcY,
  srcWidth, srcHeight   : SmallInt;
  ROpFlag               : LongInt;
Begin
{** Prepare Destanation **}
  destDC := ACanvas.Handle;
  with Rect do
   begin
     destX      := Left;
     destY      := Top;
     destWidth  := Right  - Left;
     destHeight := Bottom - Top;
   end;{with Rect do}
{** Prepare Source **}
  srcDC := fBitmap.Canvas.Handle;
  with fBitmap do
   begin
     srcX      := 0;
     srcY      := 0;
     srcWidth  := Width;
     srcHeight := Height;
   end;{with fBitmap do}
{** Set Raster Operations Flag **}
  ROpFlag := ACanvas.CopyMode;
{** StretchBlt **}
  StretchBlt(destDC, destX, destY, destWidth, destHeight,
             srcDC,  srcX,  srcY,  srcWidth,  srcHeight,
             ROpFlag);
End;{Procedure TGif.Draw}

{**************************}
{** Properties Overrides **}
{**************************}
Function TGif.GetEmpty : Boolean;
Begin
  Result := fBitmap.Empty;
End;{Function TGif.GetEmpty}

Function TGif.GetHeight : integer;
Begin
  Result := ImageDescriptor.ImageHeight;
End;{Function TGif.GetHeight}
Procedure TGif.SetHeight(A : integer);
Begin
End;{Procedure TGif.SetHeight}

Function TGif.GetWidth : integer;
Begin
  Result := ImageDescriptor.ImageWidth;
End;{Function TGif.GetWidth}
Procedure TGif.SetWidth(A : integer);
Begin
End;{Procedure TGif.SetWidth}

{*********************}
{** Streams Routine **}
{*********************}
Procedure TGif.ReadData(Stream : TStream);
Var
  Size: LongInt;
Begin
  Stream.Read(Size, SizeOf(Size));
  ReadStream(Size, Stream);
  CheckObjects;
  ConvertGif;
  Changed(Self);
End;{Procedure TGif.ReadData}

Procedure TGif.WriteData(Stream : TStream);
Begin
  WriteStream(Stream, True);
End;{Procedure TGif.WriteData}

{******************************************************************************}
{** Private *******************************************************************}
{******************************************************************************}
{** Streams Routine **}
{*********************}
Procedure TGif.InitCompressionStream;
Begin
  fGifStream.Read(LZWCodeSize, SizeOf(LZWCodeSize)); { get minimum code size }
{** Check For Correct Code Size **}
  if (LZWCodeSize < 2) or (LZWCodeSize > 9)      { valid code sizes 2-9 bits }
   then Raise EGif.Create(strWrongCodeSize);
{** PreSet Variables **}
  CurrCodeSize := Succ(LZWCodeSize);             { set the initial code size }
  ClearCode    := (1 shl LZWCodeSize);           { set the clear code }
  EndingCode   := Succ(ClearCode);               { set the ending code }
  HighCode     := Pred(ClearCode);               { set the highest code not needing Decoding }
  BytesLeft    := 0;
  BitsLeft     := 0;
  CurrentX     := 0;
  CurrentY     := 0;
End;{Procedure TGif.InitCompressionStream}

Procedure TGif.ReadSubBlock;
Begin
{** Get Block Size **}
  fGifStream.Read(ImageData.Size, SizeOf(ImageData.Size));
{** Check For Empty Block **}
  if ImageData.Size = 0
   then Raise EGif.Create(strEmptyBlock);
{** Read In Block **}
  fGifStream.Read(ImageData.Data, ImageData.Size);
  NextByte  := 1;                                 {** Reset Next Byte  **}
  BytesLeft := ImageData.Size;                    {** Reset Bytes Left **}
End;{Procedure TGif.ReadSubBlock}

Procedure TGif.ReadStream(Size   : LongInt;
                          Stream : TStream);
Begin
  fGifStream.SetSize(Size);
  Stream.ReadBuffer(fGifStream.Memory^, Size);
End;{Procedure TGif.ReadStream}

Procedure TGif.WriteStream(Stream    : TStream;
                           WriteSize : Boolean);
Var
  Size: LongInt;
Begin
  Size := fGifStream.Size;
  if WriteSize
   then Stream.WriteBuffer(Size, SizeOf(Size));
  if Size <> 0
   then Stream.WriteBuffer(fGifStream.Memory^, Size);
End;{Procedure TGif.WriteStream}

{********************}
{** Decode Routine **}
{********************}
Procedure TGif.DecodeGifHeader;
Begin
{** Read Header **}
  fGifStream.Read(Header, SizeOf(Header));
{** Check For Right Header **}
  if Header.Signature <> strGifHeaderSignature
   then Raise EGif.Create(strNotGifFile);
{** Work Arround LogicalScreen **}
  fGifStream.Read(LogicalScreen, SizeOf(LogicalScreen));
{** Check For Color Table **}
  if (LogicalScreen.PackedFields and lsdGlobalColorTable) <> lsdGlobalColorTable
   then Raise EGif.Create(strNoGlobalColorTable);
{** Read Global Color Table **}
  TableSize := Trunc(Power(2,(LogicalScreen.PackedFields
                              and lsdColorTableSize)+1));
  fGifStream.Read(GlobalColorTable, (TableSize * SizeOf(TGifColorItem)));
{** Check For Preceded **}
  if not ProcessExtensions
   then Raise EGif.Create(strPreceded);
{** Read ImageDescriptor **}
  with fGifStream do
   begin
   {** Move Back 'couse ProcessExtensions Read ImageDescriptor.Separator Too **}
     Seek(-SizeOf(ImageDescriptor.Separator), soFromCurrent);
     Read(ImageDescriptor, SizeOf(ImageDescriptor));
   end;{with fGifStream do}
{** Check For Local Color Table **}
  if (ImageDescriptor.PackedFields
     and idLocalColorTable) = idLocalColorTable then
   begin
    {** Read Local Color Table **}
     TableSize := Trunc(Power(2,(ImageDescriptor.PackedFields
                                 and idColorTableSize)+1));
     fGifStream.Read(LocalColorTable, (TableSize * SizeOf(TGifColorItem)));
     UseLocalColors := True;
   end
  else UseLocalColors := False;
{** Check For Interlaced **}
  if (ImageDescriptor.PackedFields and idInterlaced) = idInterlaced then
   begin
     Interlaced    := True;
     InterlacePass := 0;
   end;{if (ImageDescriptor.PackedFields...}
{** Check For Stream Error **}
  if not Assigned(fGifStream)
   then Raise EGif.Create(strNoFile);
End;{Procedure TGif.DecodeGifHeader}

{*****************************************************}
{** Procedure Actually Decodes Gif Image            **}
{** Special Thancks Sean Wenzel and High Gear, Inc. **}
{*****************************************************}
Procedure TGif.DecodeGif;
Var
  SP           : SmallInt;     { index to the Decode stack }
  TempOldCode,
  OldCode      : Word;
  BufCnt       : Word;         { line buffer counter }
  Code, C      : Word;
  CurrBuf      : Word;         { line buffer index }
  MaxedOut     : Boolean;

{** Local Procedure that Decodes a code and puts it on the Decode stack **}
  Procedure DecodeCode(Var Code : Word);
  Begin
    while Code > HighCode do            { rip thru the prefix list placing suffixes }
     begin                              { onto the Decode stack }
       DecodeStack[SP] := Suffix[Code]; { put the suffix on the Decode stack }
       Inc(SP);                         { Increment Decode stack index }
       Code := Prefix[Code];            { get the new prefix }
     end;{while Code > HighCode do}
    DecodeStack[SP] := Code;            { put the last code onto the Decode stack }
    Inc(SP);                            { Increment the Decode stack index }
  End;{INTERNAL Procedure DecoeCode}

  Procedure WorkArroundClearCode;
  Begin
    CurrCodeSize := LZWCodeSize + 1;         { reset the code size }
    Slot         := EndingCode  + 1;         { set slot for next new code }
    TopSlot      := (1 shl CurrCodeSize);    { set max slot number }
  {** Read until all clear codes gone - shouldn't happen **}
    while C = ClearCode do
     C := NextCode;
  {** Check For EndingCode After Clear **}
    if C = EndingCode
     then Raise EGif.Create(strWrongCode);
  {** Set to Zero if Code is Beyond Preset Codes **}
    if C >= Slot
     then C := 0;
    OldCode := C;
  {** Output Code to Decoded Stack **}
    DecodeStack[SP] := C;
    Inc(SP);
  End;{INTERNAL Procedure WorkArroundClearCode}

  Procedure WorkArroundCodeInTable;
  Begin
    DecodeCode(Code);                  { Decode the code }
    if Slot <= TopSlot then
     begin                             { add the new code to the table }
       Suffix[Slot] := Code;           { make the suffix }
       PreFix[slot] := OldCode;        { the previous code - a link to the data }
       Inc(Slot);                      { Increment slot number }
       OldCode := C;                   { set oldcode }
     end;{if Slot <= TopSlot then}
    if Slot >= TopSlot then
     begin {** Have Reached Top Slot for Bit Size **}
       if CurrCodeSize < 12 then       { new bit size not too big? }
        begin
          TopSlot := (TopSlot shl 1);  { new top slot }
          Inc(CurrCodeSize);           { new code size }
        end
       else MaxedOut := True;
     end;{if Slot >= TopSlot then}
  End;{INTERNAL Procedure WorkArroundCodeInTable}

  Procedure WorkArroundCodeOutOfTable;
  Begin
  {** Check For Next Available Slot **}
    if Code <> Slot
     then Raise EGif.Create(strWrongCode);
  {** the code does not exist so make a new entry in the code table
      and then translate the new code ** }
    TempOldCode := OldCode;                { make a copy of the old code }
    while OldCode > HighCode do            { translate the old code and place it }
     begin                                 { on the Decode stack }
       DecodeStack[SP] := Suffix[OldCode]; { do the suffix }
       OldCode         := Prefix[OldCode]; { get next prefix }
     end;{ while OldCode > HighCode do}
  {** put the code onto the Decode stack but DO NOT Increment stack
      index because because we are only translating the oldcode to get
      the first Character  **}
    DecodeStack[SP] := OldCode;

    if Slot <= TopSlot then
     begin                                { make new code entry }
       Suffix[Slot] := OldCode;           { first Char of old code }
       Prefix[Slot] := TempOldCode;       { link to the old code prefix }
       Inc(Slot);                         { Increment slot }
     end;{if Slot <= TopSlot then}

    if Slot >= TopSlot then               { slot is too big }
     begin                                { Increment code size }
       if CurrCodeSize < 12 then
        begin
          TopSlot := (TopSlot shl 1);     { new top slot }
          Inc(CurrCodeSize);              { new code size }
        end
       else MaxedOut := True;
     end;{if Slot >= TopSlot then}

  {** Now that the table entry exists Decode it set the new old code **}
    DecodeCode(Code);
    OldCode := C;
  End;{INTERNAL Procedure WorkArroundCodeOutOfTable}

  Procedure PutToLineBuffer;
  Begin
    while SP > 0 do
     begin
       Dec(SP);
       LineBuffer[CurrBuf] := DecodeStack[SP];
       Inc(CurrBuf);
       Dec(BufCnt);
       if BufCnt = 0 then
        begin {** Line is Full **}
          DrawGifLine;
          CurrBuf := 0;
          BufCnt := ImageDescriptor.ImageWidth;
        end;{if BufCnt = 0 then}
     end;{while SP > 0 do}
  End;{INTERNAL Procedure PutToLineBuffer}

Begin
{** Initialize Decoding Paramaters **}
  InitCompressionStream;
{** PreSet Variables **}
  OldCode  := 0;
  SP       := 0;
  BufCnt   := ImageDescriptor.ImageWidth; {** Set Image Width **}
  CurrBuf  := 0;
  MaxedOut := False;
{** Run Thru Loop **}
  C := NextCode;                                 { get the initial code - should be a clear code }
  while C <> EndingCode do                       { main loop until ending code is found }
   begin
     if C <> ClearCode then
      begin {** Code Must be Decoded **}
        Code := C;
        if Code < Slot
         then WorkArroundCodeInTable
         else WorkArroundCodeOutOfTable;
      end
     else WorkArroundClearCode;
   {** the Decoded String is on the Decode stack so pop it off and put it
       into the line buffer **}
     PutToLineBuffer;
   {** Get Next Code **}
     C := NextCode;
   {** Check For Error**}
     if (MaxedOut) and (C <> ClearCode)
      then Raise EGif.Create(strWrongBitSize);
     MaxedOut := False;
   end;{while C <> EndingCode do}
End;{Procedure TGif.DecodeGif}

{*********************}
{** Process Routine **}
{*********************}
Procedure TGif.CheckObjects;
Begin
  if not Assigned(fGifStream)
   then fGifStream := TMemoryStream.Create;
  if not Assigned(fBitmap)
   then fBitmap := TBitmap.Create;
  if not Assigned(fBitmapStream)
   then fBitmapStream := TMemoryStream.Create;
  if not Assigned(fBitmapLineList)
   then fBitmapLineList := TList.Create;
End;{Procedure TGif.CheckObjects}

Procedure TGif.DrawGifLine;
Var
  NewLine : TBitmapLine;
Begin
{** Rather than writing the image line to the screen, we're going to instantiate
    a bitmap line and put the line there. **}
  NewLine := TBitmapLine.Create;
  with NewLine do
   begin
     BitmapLine := LineBuffer;
     LineNumber := CurrentY;
   end;{with NewLine do}
{** Add New Line **}
  fBitmapLineList.Add(NewLine);
	Inc(CurrentY);
{** Work Arround Interlaced **}
	if Interlaced then
   begin
   {** Incremental Process **}
     case InterlacePass of
       0: Inc(CurrentY, 7);
       1: Inc(CurrentY, 7);
       2: Inc(CurrentY, 3);
       3: Inc(CurrentY, 1);
     end;{case InterlacePass of}
   {** Check Out Of Image **}
     if CurrentY >= ImageDescriptor.ImageHeight then
      begin
        Inc(InterlacePass);
        case InterlacePass of
          1: CurrentY := 4;
          2: CurrentY := 2;
          3: CurrentY := 1;
        end;{case InterlacePass of}
      end;
   end;{if Interlaced then}
End;{Procedure TGif.DrawGifLine}

Function TGif.ProcessExtensions : Boolean;
Var
  AExtensionBlock           : TGifExtensionBlock;
  AGraphicsControlExtension : TGifGraphicsControlExtension;
  APlainTextExtension       : TGifPlainTextExtension;
  AApplicationExtension     : TGifApplicationExtension;

  Procedure ProcessSubBlocks;
  Var
    ASubBlock : TGifDataSubBlock;
  Begin
  {** Get Data Block Size **}
    fGifStream.Read(ASubBlock.Size, SizeOf(ASubBlock.Size));
    while ASubBlock.Size <> 0 do
     begin
       fGifStream.Read(ASubBlock.Data, ASubBlock.Size);
       fGifStream.Read(ASubBlock.Size, SizeOf(ASubBlock.Size));
     end;{while ASubBlock.Size <> 0 do}
  End;{INTERNAL Procedure ProcessSubBlocks}

  Procedure ProcessGraphicControl;
  Begin
    fGifStream.Read(AGraphicsControlExtension,
                    SizeOf(AGraphicsControlExtension));
  End;{INTERNAL Procedure ProcessGraphicControl}

  Procedure ProcessComment;
  Begin
    ProcessSubBlocks;
  End;{INTERNAL Procedure ProcessComment}

  Procedure ProcessApplication;
  Begin
    fGifStream.Read(AApplicationExtension,
                    SizeOf(AApplicationExtension));
    ProcessSubBlocks;
  End;{INTERNAL Procedure ProcessApplication}

  Procedure ProcessPlainText;
  Begin
    fGifStream.Read(APlainTextExtension,
                    SizeOf(APlainTextExtension));
    ProcessSubBlocks;
  End;{INTERNAL Procedure ProcessPlainText}

Begin
  Result := True;
{** Read Image Descriptor Separator **}
  fGifStream.Read(ImageDescriptor.Separator,
                  SizeOf(ImageDescriptor.Separator));
{** Run Thru Loop  **}
  while (ImageDescriptor.Separator <> ImageSeparator) do
   if (ImageDescriptor.Separator = ceExtensionIntroducer) then
    begin
    {** Read ExtensionLabel **}
      fGifStream.Read(AExtensionBlock.ExtensionLabel,
                      SizeOf(AExtensionBlock.ExtensionLabel));
    {** Separate Process by ExtensionLabel **}
      case (AExtensionBlock.ExtensionLabel) of
       cePlainTextLabel            : ProcessPlainText;
       ceGraphicControlLabel       : ProcessGraphicControl;
       ceCommentLabel              : ProcessComment;
       ceApplicationExtensionLabel : ProcessApplication;
      end;{case AExtensionBlock.ExtensionLabel of}
    {** Read Separator **}
      fGifStream.Read(ImageDescriptor.Separator,
                      SizeOf(ImageDescriptor.Separator));
    end
   else Result := False;
End;{Function TGif.ProcessExtensions}

{** Returns Code of The Proper Bit Size **}
Function TGif.NextCode : Word;
Begin
  if BitsLeft = 0 then
   begin
   {** Check for Another Block **}
     if BytesLeft <= 0
      then ReadSubBlock;
     CurrByte := ImageData.Data[NextByte]; { get a byte }
     Inc(NextByte);                        { set the next byte index }
     BitsLeft := 8;                        { set bits left in the byte }
     Dec(BytesLeft);                       { Decrement the bytes left counter }
   end;{if BitsLeft = 0 then}

  Result := CurrByte shr (8 - BitsLeft);  { shift off any previosly used bits}
  while CurrCodeSize > BitsLeft do               { need more bits ? }
   begin
   {** Check For Bytes Left In Block **}
     if BytesLeft <= 0
      then ReadSubBlock;
     CurrByte := ImageData.Data[NextByte];         { get another byte }
     Inc(NextByte);                                { Increment NextByte counter }
     Result   := Result or (CurrByte shl BitsLeft);{ add the remaining bits to the return value }
     Inc(BitsLeft, 8);                              { set bit counter }
     Dec(BytesLeft);                               { Decrement bytesleft counter }
   end;{while CurrCodeSize > BitsLeft do}

  BitsLeft := BitsLeft - CurrCodeSize;             { subtract the code size from bitsleft }
  Result   := (Result and CodeMask[CurrCodeSize]); { mask off the right number of bits }
End;{Function TGif.NextCode}

{*********************}
{** Convert Routine **}
{*********************}
Procedure TGif.ConvertGif;

  Procedure DeleteLinesAndClearList;
  Var
    TempLine : TBitmapLine;
    i        : integer;
  Begin
    if fBitmapLineList.Count > 0 then
     for i := (fBitmapLineList.Count - 1) downto 0 do
      begin
        TempLine := fBitmapLineList.Items[i];
        fBitmapLineList.Delete(i);
        TempLine.Free;
      end;{for i := (fBitmapLineList.Count - 1) downto 0 do}
    fBitmapLineList.Clear;
  End;{INTERNAL Procedure DeleteLinesAndClearList}

Begin
{** Staring Decoding **}
  CheckObjects;
  DecodeGifHeader;
{** ReCreate Lines List If Needed **}
  if not Assigned(fBitmapLineList)
   then fBitmapLineList := TList.Create;
{** Free Lines List**}
  DeleteLinesAndClearList;
{** Set New List Size (Capacity) **}
  fBitmapLineList.Capacity := ImageDescriptor.ImageHeight;
{** Gif To BMP**}
  DecodeGif;
  ConvertGifToBmp;
{** Free Lines List**}
  DeleteLinesAndClearList;
End;{Procedure TGif.ConvertGif}


Procedure TGif.ConvertGifToBmp;
Var
  ABitmapFileHeader : TBitmapFileHeader;
  ARGDQuad          : TRGBQuad;
  i, ImageWidth,
  BoundarySize      : integer;
Const
  Bounder : LongInt     = $00000000;
Begin
{** Prepare Bitmap Info Header **}
  with fBitmapInfoHeader do
   begin
     biSize          := SizeOf(fBitmapInfoHeader);
     biWidth         := ImageDescriptor.ImageWidth;
     biHeight        := ImageDescriptor.ImageHeight;
     biPlanes        := 1;
     biBitCount      := 8;
     biCompression   := BI_RGB; {** Not Compressed Bitmap **}
     biSizeImage     := 0;
     biXPelsPerMeter := 143;
     biYPelsPerMeter := 143;
     biClrUsed       := 0;
     biClrImportant  := 0;
   end;{with fBitmapInfoHeader do}

{** Set Image Size And Calculate Boundary Size **}
  ImageWidth   := ImageDescriptor.ImageWidth;
  BoundarySize := ImageWidth mod 4;
  if BoundarySize <> 0
   then BoundarySize := 4 - BoundarySize;

{** Prepare Bitmap File Header **}
  with ABitmapFileHeader do
   begin
     bfType      := bmpFileSignature;
     bfOffBits   := 1024 + {** Palettte **}
                    SizeOf(ABitmapFileHeader) +
                    SizeOf(fBitmapInfoHeader);
     bfSize      := bfOffBits +
                    (ImageDescriptor.ImageHeight *
                    (ImageDescriptor.ImageWidth + BoundarySize));
     bfReserved1 := 0;
     bfReserved2 := 0;
   end;{with ABitmapFileHeader do}

{** Check fBitmapStream**}
  if not Assigned(fBitmapStream)
   then fBitmapStream := TMemoryStream.Create;

{** Write To fBitmapStream **}
  with fBitmapStream do
   begin
     Clear;
   {** Write Headers **}
     Write(ABitmapFileHeader, SizeOf(ABitmapFileHeader));
     Write(fBitmapInfoHeader, SizeOf(fBitmapInfoHeader));
   {** Write RGB Palette **}
     ARGDQuad.rgbReserved := 0; {** Preset Reserved Byte **}
     if UseLocalColors then
      for i:=0 to 255 do
       begin
         with ARGDQuad do
          begin
            rgbRed   := LocalColorTable[i].Red;
            rgbGreen := LocalColorTable[i].Green;
            rgbBlue  := LocalColorTable[i].Blue;
          end;{with ARGDQuad do}
         Write(ARGDQuad, SizeOf(ARGDQuad));
       end{for i:=0 to 255 do}
     else
      for i:=0 to 255 do
       begin
         with ARGDQuad do
          begin
            rgbRed   := GlobalColorTable[i].Red;
            rgbGreen := GlobalColorTable[i].Green;
            rgbBlue  := GlobalColorTable[i].Blue;
          end;{with ARGDQuad do}
         Write(ARGDQuad, SizeOf(ARGDQuad));
       end;{for i:=0 to 255 do}

   {** Sort List if Needed **}
     if Interlaced
      then fBitmapLineList.Sort(SortBitmapLineList);
   {** Write All Lines to Stream (Reverse Order) **}
     for i := (fBitmapLineList.Count - 1) downto 0 do
      begin
        Write(TBitmapLine(fBitmapLineList.Items[i]).BitmapLine, ImageWidth);
      {** Additional Zeros for Right BMP Line Size (MUST BE 32 Bit Aligned) **}
        Write(Bounder, BoundarySize);
      end;{for i := (fBitmapLineList.Count - 1) downto 0 do}
   {** Reset Stream **}
     Seek(0, soFromBeginning);
   end;{with fBitmapStream do}

{** Reload Bitmap from Stream **}
  fBitmap.LoadFromStream(fBitmapStream);
End;{Procedure TGif.ConvertGifToBmp}


{##############################################################################}
{******************************************************************************}
{##############################################################################}
Initialization
  RegisterClass(TGif);
{$IfDef AntUnits_UseGif}
  TPicture.RegisterFileFormat('GIF', 'GIF Image File', TGif);
{$EndIf AntUnits_UseGif}

{##############################################################################}
{******************************************************************************}
{##############################################################################}
Finalization
{$IfDef Delphi3andHigher}
  {$IfDef AntUnits_UseGif}
  TPicture.UnregisterGraphicClass(TGif);
  {$EndIf AntUnits_UseGif}
{$EndIf Delphi3andHigher}

END{Unit AntGif}.
