{$I _hdr.inc}
unit userlist;
interface uses Classes, PackUnit, Tools;

type
 TUserStatus = (uLocal, uOK, uNotResponding, uNotExists);


 PAddressList = ^TAddressList;
 TAddressList = array[0..MaxPlugins] of TAddress;

 PUserInfo = ^TUserInfo;
 TUserInfo = record
               UserName:        TUserName;
               UserStatus:      TUserStatus;
               Computer:        String[127]; // only for user, ripped from some TAddress
               LastResponse:    TDateTime;
               AddressList:     PAddressList;
               AListSize:       byte;
               Addresses:       array [0..MaxPlugins] of byte;
             end;

type

 TUserList = class(TList)
 private
  FChanged:     boolean;
  FLocalUser:   TUserInfo;
  function      GetChanged: boolean;
  procedure     SetAddress(UserInfo: PUserInfo;Addr: TAddress);
  procedure     Delete(Index: Integer);
  function      GetLocalUser: TUserName;
 protected
 public
  property      Changed: boolean read GetChanged;
  property      LocalUser: TUserName read GetLocalUser;
  constructor   Create;
  procedure     SetLocalUser(Nick: TUserNick);
  function      UserStatus(const Nick: TUserName): TUserStatus;
  function      GetUserName(const Address: TAddress): TUserName;
  procedure     ReceiveUser(XPacket: TPacket); // amUserName
  procedure     DeleteUser(XPacket: TPacket);  // amUserKO
  function      NickEmpty: boolean;
  procedure     WaitForRefresh;
 end;

var
 LANCHUsers: TUserList;

implementation uses MainUnit, SysUtils {$IFDEF DEBUG}, Tools{$ENDIF};

function TUserList.GetChanged: boolean;
begin
 RESULT:=FChanged;
 FChanged:=false;
end;

procedure TUserList.SetLocalUser(Nick: TUserNick);
var n, n2: string[8];
begin
 n:=IntToStr(Random(65535));
 while (n[0] < #8) do n:=n+'0';
 n2:=IntToStr(Random(65535)); // >>> time stamp, not random
 while (n2[0] < #8) do n2:=n2+'0';
 FLocalUser.UserName:=n+n2+'/'+Nick;
end;

function TUserList.GetLocalUser: TUserName;
begin
 RESULT:=FLocalUser.UserName;
end;

function TUserList.NickEmpty: boolean;
begin
 RESULT:=(Length(FLocalUser.UserName) > UserNamePrefix);
end;

procedure TUserList.WaitForRefresh;
var I: integer;
    r: PUserInfo;
begin
 for I:=0 to (Count-1) do begin
  r:=Items[I];
  r^.UserStatus:=uNotResponding;
 end;{for}
end;

procedure TUserList.SetAddress(UserInfo: PUserInfo;Addr: TAddress);
var ANum: byte;
begin
 ANum:=Addr.Com;
 if (UserInfo^.AListSize <= ANum) then ReallocMem(UserInfo^.AddressList, (ANum+1) * SizeOf(TAddress));
 UserInfo^.AListSize:=ANum+1;
 UserInfo^.Addresses[ANum] := 1;
 UserInfo^.AddressList^[ANum]:=Addr;
end;

function TUserList.GetUserName(const Address: TAddress): TUserName;
var I: integer;
    r: PUserInfo;
    ANum: byte;
begin
 ANum := Address.Com;
 RESULT:='';
 for I:=0 to (Count-1) do begin
  r:=Items[I];
  if (r^.AListSize > ANum) and (r^.AddressList^[ANum].S = Address.S) then
   RESULT:=r^.UserName;
 end;{for}
end;

procedure TUserList.ReceiveUser(XPacket: TPacket);
var
 Nick:  ShortString;
 i:     integer;
 r:     PUserInfo;
 f:     boolean;
begin
 Nick:=UpperCase(XPacket.SenderN);
 f:=false;
 for I:=0 to (Count-1) do begin
  r:=Items[I];
  if (UpperCase(r^.UserName) = Nick) then begin
   r^.LastResponse:=Now;
   r^.UserStatus:=uOK;
   f:=true;
   BREAK;
  end;{if}
 end;{for}
 if (not f) then begin
  New(r);
  SetAddress(r, XPacket.SenderA);
  r^.UserName:=XPacket[1];
  r^.LastResponse:=Now;
  r^.UserStatus:=uOK;
  Add(r);
  FChanged:=true;
 end;
end;

procedure TUserList.DeleteUser(XPacket: TPacket);
var I: integer;
    Nick: string[31];
    r: PUserInfo;
begin
 Nick:=UpperCase(XPacket.SenderN);
 for I:=0 to (Count-1) do begin
  r:=Items[I];
  if (Nick = UpperCase(r^.UserName)) then begin
   Delete(I);
   BREAK;
  end;{if}
 end;{for}
end;

procedure TUserList.Delete(Index: Integer);
var r: PUserInfo;
begin
 R:=Items[Index];
 ReallocMem(R^.AddressList,0);
 Dispose(R);
 FChanged:=true;
 inherited;
end;

function TUserList.UserStatus(const Nick: TUserName): TUserStatus;
var i: integer;
    N: ShortString;
begin
 N:=UpperCase(Nick);
 RESULT:=uNotExists;
 if (N = UpperCase(FLocalUser.UserName)) then
   RESULT:=uLocal
 else begin
  for I:=0 to (Count-1) do
   if (UpperCase(PUserInfo(Items[I])^.UserName) = N) then RESULT:=uOK;
 end;{else}
end;

constructor TUserList.Create;
begin
 inherited;
end;

initialization
 LANCHUsers:=TUserList.Create;
finalization
 LANCHUsers.Free;
end.
