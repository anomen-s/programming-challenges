{$I _hdr.inc}
unit BigFiles;

interface uses Classes, PackUnit, Tools;

const
 stComplete	=   1;
 stSending	=   2;
 stReceiving	=   4;
 stRemote	= $10;
 stInvalidCRC	= $20;

type
 TFile = class;

 TFile = class(TObject)
   Status:	integer;
   FileName:	shortstring;
   Data:	pointer;	// always (Coca Cola)
   Size:	integer;	// -//-
   CRC:		cardinal;
   DirStream:	TMemoryStream;
   Packet:      TPacket;
   FileList:	TStrings; // offset (8 bytes - hexa num) / length (8B - hex) / file name
                         // is send in block $FFffFFff
	{ ********************************** }
   function	Save: boolean;
   constructor	LoadFile(const FName: shortstring);
   constructor	LoadDir(const Path: shortstring);
   constructor	CreateRemote(const FName: Shortstring);
   destructor	Destroy;override;
        { TSendFile }
   procedure	Send(const GP, Dest: TUserName;ID: cardinal);
        { TReceiveFile }
   constructor	ReceiveFile(XPacket: TPacket);
 private
   procedure 	SaveDir(const Base: ShortString);
//   function	BlockAddr(Block: integer;var BSize: integer): pointer;
//   function	BlockCount: word;
   procedure 	ScanDir(const DirectoryPath: ShortString;var Base: shortstring);
   procedure 	AddFile(Name: ShortString; var Base: shortstring);
 end;


implementation uses ErrorF, Windows, DirDlg, MainUnit, FileCtrl, SysUtils{$IFDEF DEBUG}, Debug{$ENDIF};

(*****************************************************************)
(************************  T F I L E  ****************************)
(*****************************************************************)

constructor TFile.CreateRemote(const FName: ShortString);
begin
 inherited Create;
 Status:=stRemote;
 FileName:=FName;
 {$IFDEF DEBUG}BreakIf((Data <> nil) or (Size <> 0) or (Packet <> nil),
	'Neni smazana pamet v TFile.CreateRemote');
 {$ENDIF}
end;


// requires: 	TPacket.Lines <> 0
//		IDCode, D_Computer set
procedure TFile.Send(const GP, Dest: TUserName;ID: cardinal);
var p: pointer;
begin
 // >> add some status checking
 Packet.NewPacket(ID,
        GP+CRLF+                   // 0-1  GP
        FileName+CRLF+             // 2 File name
        IntToStr(Size)+CRLF+       // 3 file size
        IntToStr(CRC));            // 4 CRC
 Packet.SetData(Data,Size);
 Packet.SendToUser(Dest);
 Packet.Clear;
end;

constructor TFile.LoadFile(const FName: shortstring);
var Stream: TFileStream;
begin
 inherited Create;
 Stream:=TFileStream.Create(FName, fmOpenRead or fmShareDenyWrite);
 FileName:=ExtractFileName(FName);
try
 Packet:=TPacket.Create;
 Status:=stComplete;
 Size:=Stream.Size;
 GetMem(Data, Size);
 Stream.Read(Data^, Size);
 CRC:=not CalcCRC(cardinal(-1), Self.Data^,Self.Size);{ calc CRC }
finally
 Stream.Free;
end;{try/f}
end;

function TFile.Save: boolean;
var WStream: TFileStream;
    Path: shortstring;
begin
 RESULT:=true;
 if ((Status and stInvalidCRC) <> 0) and (Windows.MessageBox(MainForm.Handle,'Chcete soubor uložit, i když má chybný souèet CRC ?','LANCHmeAT', MB_ICONSTOP or MB_YESNO) = IDNO)
   then EXIT;

 if (FileName[1] <> '\') then begin	 	// file
  MainForm.SaveDlg.FileName:=FileName;
  MainForm.SaveDlg.Filter:=LoadStr(STR_AllFiles);
  if MainForm.SaveDlg.Execute then
   try
    WStream:=TFileStream.Create(MainForm.SaveDlg.FileName, fmCreate or fmShareDenyWrite);
    WStream.Write(Data^, Size);
    WStream.Free;
   except
    CriticalError('Nepovedlo se uložit soubor');
    RESULT:=false;
   end;{try/e}
 end{if}
 else begin				//directory
//  CriticalError('Tato verze ještì neumí pracovat s adresáøi');EXIT;
  Path:=BrowseDirectoryMP('Zvolte adresáø:');
  if (Path <> '') then SaveDir(Path);

 end;{else}
end;

Destructor TFile.Destroy;
begin
try	// DATA
 if (Data <> nil) then
 try FreeMem(Data);
 except{$IFDEF DEBUG}BreakIf(true,'chyba pri uvolnovani TFile.Data ');{$ENDIF}
 end;{try/e}
        // FILELIST
 if (FileList <> nil) then
 try FileList.Clear;FileList.Free;
 except{$IFDEF DEBUG}BreakIf(true,'chyba pri demolovani TFile.FileList');{$ENDIF}
 end;{try/e}
        // PACKET.LINES
 if (Packet <> nil) then
 try Packet.Free;
 except{$IFDEF DEBUG}BreakIf(true,'chyba pri demolovani TFile.Packet.Lines');{$ENDIF}
 end;{try/e}
finally
 inherited ;
end;{try/f}
end;

(*****************************************************************)
(*****************************************************************)
(************  T R e c e i v e F i l e  **************************)
(*****************************************************************)
(*****************************************************************)


constructor TFile.ReceiveFile(XPacket: TPacket);
begin
  //
end;




/////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////

(*Function IsDir(Atribut: Integer): Boolean;
var Atr: Boolean;
begin
 Atr:=False;
 if (Atribut and faDirectory) = faDirectory then Atr:=true;
 Case Atribut of
  $10: Atr:=True;             { faDirectory                     }
  $12: Atr:=True;             { faDirectory+faHidden            }
  $30: Atr:=True;             { faArchive+faDirectory           }
  $810, $830, $16: Atr:=True; { faDirectory + Asi sitove veci ? }
  $32: Atr:=True;             { faArchive+faDirectory+faHidden  }
 end;{case}
 RESULT:=Atr;
end;   *)

procedure TFile.AddFile(Name: ShortString;var Base: shortstring);
var Stream: TFileStream;
    TmpData: Pointer;
    P, S: integer;
begin
try
 Stream:=TFileStream.Create(Name, fmOpenRead or fmShareDenyWrite);
 S:=Stream.Size;
 GetMem(TmpData, S);
 Stream.Read(TmpData^, S);
 Stream.Free;
 P:=DirStream.Position;
 Self.DirStream.Write(TmpData^, S);
 {$IFDEF DEBUG}BreakIf(Base <> copy(Name,1,byte(Base[0])),'Invalid base path!');{$ENDIF}
 Delete(Name, 1, byte(Base[0]));
 Self.FileList.Add(IntToHex(P,8)+IntToHex(S,8)+Name);
except
 ErrorF.Error('Soubor: '+Name);
 EXIT;
end;{try/e}
end;

procedure TFile.ScanDir(const DirectoryPath: ShortString;var Base: shortstring);
var SearchRec: TSearchRec;
    Result: Integer;
begin
 Result := SysUtils.FindFirst(DirectoryPath+'*.*', faAnyFile, SearchRec);
 while (Result = 0) do begin
   if (SearchRec.Name[1]<>'.') then
    if ((SearchRec.Attr and faDirectory) = faDirectory) then
      Self.ScanDir(DirectoryPath{+'\'}+SearchRec.Name+'\', Base)
     else begin
{$IFDEF DEBUG}ErrorF.Error(DirectoryPath+SearchRec.Name);{$ENDIF}
      Self.AddFile(DirectoryPath+SearchRec.Name, Base);{.. filename }
     end;{else}
   Result:=SysUtils.FindNext(SearchRec);
 end;{while}
 SysUtils.FindClose(SearchRec);
end;


constructor TFile.LoadDir(const Path: shortstring);
var DirName: shortstring;
begin
 inherited Create;
// raise Exception.Create('Tohle jeste neni hotovy');
 DirStream:=TMemoryStream.Create;
 Packet:=TPacket.Create;
 FileList:=TStringList.Create;
 Status:=stComplete;
 DirName:=Path;
 FileName:='\'+ExtractFileName(Path);
 if (Path[Length(Path)] <> '\') then DirName:=DirName+'\';
 ScanDir(DirName, DirName);
 Self.Size:=DirStream.Size;
 GetMem(Self.Data, Self.Size);
 Move(DirStream.Memory^, Self.Data^, Self.Size);
 DirStream.Free;
 CRC:=not CalcCRC(cardinal(-1),Self.Data^,Self.Size);
 {calc CRC }
end;

procedure TFile.SaveDir(const Base: ShortString);
var P, S, Index: integer;
    Buf: pointer;
    CurrFile: ShortString;
    WStream: TFileStream;
begin
 for Index:=0 to (FileList.Count-1) do begin
  {$IFDEF DEBUG}BreakIf(Length(FileList[Index])<18,'Invalid FileList item');{$ENDIF}
  P:=HexToInt(Copy(FileList[Index],1,8));
  S:=HexToInt(Copy(FileList[Index],9,8));
  Buf:=pointer(integer(Data)+P);
  CurrFile:=AddBSlash(Base)+Copy(FileList[Index],17,Length(FileList[Index]));
  {$IFDEF DEBUG}BreakIf(not{$ENDIF}ForceDirectories(CurrFile)
  {$IFDEF DEBUG},'Cannot create dir'){$ENDIF};
  WStream:=TFileStream.Create(CurrFile, fmCreate or fmShareDenyWrite);
  WStream.Write(Buf^, S);
  WStream.Free;
 end;{for}
end;

end.
