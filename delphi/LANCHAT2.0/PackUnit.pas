{$I _hdr.inc}
unit PackUnit;

interface uses Windows, classes, Tools;

type

 TPacket = class(TStringList)
  private
   public
    SenderA:    TAddress;
    SenderN:    TUserName;
    IDCode:	cardinal;
    DataSize:	integer;
    Data:	pointer;
    procedure   Empty;          // free data, clear vars
    procedure   Clear;override; // clear variables
    procedure   SetData(Buffer: pointer;Size: integer);
    procedure   NewPacket(ID: cardinal;const Lines: ANSIString);
    procedure   SendToUser(const Dest: TUserName);
    procedure   SendToAddr(Dest: TAddress); { move to private >>>}
    procedure   Broadcast;
    destructor  Destroy;override;
 end;

function IsNewMessage: boolean;
function ReceiveMessage(Packet: TPacket): boolean;

implementation uses SysUtils, ErrorF, userList {$IFDEF DEBUG}, Debug{$ENDIF};

(*****************************************************************)
(*****************************************************************)

procedure TPacket.SetData(Buffer: pointer;Size: integer);
begin
 Data:=Buffer;
 DataSize:=Size;
 {$IFDEF DEBUG}BreakIf((Size = 0) xor (Buffer = nil),'Chybna data v TPacket.SetData!');{$ENDIF}
end;

procedure TPacket.Clear;
begin
// Text:=''; stupid mistake 
 SenderN:='';
 FillChar(SenderA, SizeOf(SenderA), 0);
 IDCode:=0;
 DataSize:=0;
 Data:=nil;
 inherited;
end;

Procedure TPacket.Empty;
begin
 if (Data <> nil) then
   try       FreeMem(Data);
   finally   Data:=nil;
   end;{TRY/F}
 Clear;
end;

procedure TPacket.NewPacket(ID: cardinal;const Lines: ANSIString);
begin
 Self.Empty;
 Self.IDCode:=ID;
 Self.Text:=Lines;
end;

destructor TPacket.Destroy;
begin
 Self.Empty;
 inherited;
end;

procedure TPacket.SendToUser(const Dest: TUserName);
begin
// Self.SendToAddr();
end;

procedure TPacket.SendToAddr(Dest: TAddress);
begin
 self.SenderN:=LANCHUsers.LocalUser;
// CRC:=CalcCRC(
 // fill SenderN
 //  timestamp, number, crc
 //  vyber kom. modulu

end;

procedure TPacket.Broadcast;
begin
 // fill Sender
 //  timestamp, number, crc
 //  vyber kom. modulu

end;

function IsNewMessage: boolean;
begin
 // >>>
end;

function ReceiveMessage(Packet: TPacket): boolean;
begin
 // >>>
end;

end.

