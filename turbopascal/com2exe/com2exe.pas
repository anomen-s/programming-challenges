{$G+,I+,R-,Q-,S-}
type
 THdr = record
         MZSign:        word;   { 5a4d }
         LastPage:      word;   { 0xxx }
         Pages:         word;   { 00yy }
         RelocCount:    word;   { 0000 }
         HdrSize:       word;   { 00xx }
         MinHeap:       word;   { 0000 }
         MaxHeap:       word;   { FFFF }
         SS:            word;   { 0000 }
         SP:            word;   { FFFE }
         Checksum:      word;   { 0000 }
         IP:            word;   { xxxx }
         CS:            word;   { 0000 }
         RelocOfs:      word;   { 001C }
         OverlayNum:    word;   { 0000 }
         RelocT:        longint;{ align to para }
 end;
const
  Hdr: THdr = ( MZSign: $5a4d;
                LastPage: 0;    Pages: 0;
                RelocCount: 0;
                HdrSize: 0;
                MinHeap: $1000; MaxHeap: $FFFF;
                SS: 000;        SP: $FFFE;
                Checksum: 0;
                IP: 0;          CS: 00;
                RelocOfs: $1C;
                OverLayNum: 0;
                RelocT: 0
                );
var
 COMFile: pointer;
 COMSize: word;
 TXTFile: pointer;
 TXTSize: word;
 RES:     word;
 EXESize: word;
 F: file;
 FI, FO, FT: string;

const NULL: longint = 0;

procedure Loader;external;{$L loader.obj}

begin
  writeln;
  WriteLn('COM2EXE');
  Writeln;
  if ParamStr(3) = '' then
   begin
    WriteLn('Syntax is');
    WriteLn('  com2exe COM_file message_file EXE_file');
    HALT(26);
   end;
  FI:=ParamStr(1);
  FT:=ParamStr(2);
  FO:=ParamStr(3);

  Assign(F,FI);                         { Load COM }
  Reset(F, 1);
  COMSize:=FileSize(F);
  if (COMSize > 65520) then begin Writeln('COM file too large !');HALT(38);end;
  GetMem(COMFile, COMSize+1);
  BlockRead(F, COMFile^, COMSize, RES);
  Close(F);

  Assign(F, FT);                        { Load Message }
  Reset(F,1);
  TXTSize:=FileSize(F);
  if (TXTSize > 32768) then begin Writeln('Message file too large !');HALT(38);end;
  if ((TXTSize and $0F) <> 0) then TXTSize:=(TXTSize and $FFF0)+$10;
  GetMem(TXTFile, TXTSize+1);
  FillChar(TXTFile^, TXTSize,#0);
  BlockRead(F, TXTFile^, FileSize(F), RES);
  Close(F);

  Hdr.HdrSize:=2+(TXTSize shr 4);   { Fill Header }
  EXESize:=COMSize+(Hdr.HdrSize shl 4) + 32;
  Hdr.LastPage:=EXESize and $1FF;
  Hdr.Pages:=EXESize shr 9;
  if (Hdr.LastPage <> 0) then Inc(Hdr.Pages);
  Hdr.IP:=COMSize;

  Assign(F, FO);                        { Write EXE }
  Rewrite(F,1);
  BlockWrite(F, Hdr, SizeOf(Hdr), RES);
  BlockWrite(F, TXTFile^, TXTSize, RES);
  BlockWrite(F, COMFile^, COMSize, RES);
  BlockWrite(F, byte(@Loader^), 32, RES);
  Close(F);

end.
