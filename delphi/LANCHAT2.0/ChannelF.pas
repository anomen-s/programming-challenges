{$I _hdr.inc}
unit ChannelF;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms,
  Dialogs, Menus, StdCtrls, ExtCtrls, Buttons,
  FileList, ComCtrls, PackUnit, Tools;

type
  TChannelForm = class(TForm)
    ChatBox: 	TMemo;
    ServerMenu: TPopupMenu;
    SMenuSave: 	TMenuItem;
    SMenuSendFile: TMenuItem;
    SMenuClose: TMenuItem;
    SMenuIgnoreLogin: TMenuItem;
    MenuNs: 	TMenuItem;
    SMenuIgnoreFiles: TMenuItem;
    SMenuIgnoreDnlds: TMenuItem;
    ChatEdit: 	TComboBox;
    SMenuSendDir: TMenuItem;
    SMenuKick: TMenuItem;
    SMenuSendTxt: TMenuItem;
    SMEnuSend:  TMenuItem;
    SMenuFiles: TMenuItem;
    Uivatel1:   TMenuItem;
    StatusBar1: TStatusBar;
    procedure 	ChatEditKeyPress(Sender: TObject; var Key: Char);
    procedure 	SaveChat(Sender: TObject);
    procedure 	Death(Sender: TObject);
    procedure 	RestrictClick(Sender: TObject);
    procedure 	FormResize(Sender: TObject);
    procedure 	FormClose(Sender: TObject; var Action: TCloseAction);
    procedure 	ChatBoxKeyPress(Sender: TObject; var Key: Char);
    procedure 	SendDir(Sender: TObject);
  private
    SelfGP:     ShortString;
    FGrpName:	ShortString;
    FIsServer:  boolean;
    Active:	boolean;
    Password:	shortstring;
    Users: 	TStringList;
    Msgs:	TStringList;
    Files:	TFileList; // for both c & s / client files have stRemote
    Packet:     TPacket;
    ServerNick: TUserName;
    Opt_Login:	boolean;
    Opt_Files:	boolean;
    Opt_Dnload:	boolean;
    procedure   PaintBackground(var Message: TMessage);message WM_ERASEBKGND;
    procedure 	cReceiveMessage(var XPacket: TPacket);
    procedure 	sReceiveMessage(var XPacket: TPacket);
    procedure 	SendToUsers;
    procedure 	SendFile(Sender: TObject);
    procedure 	SetMessage(const Msg: string;Index: integer);
    procedure 	sCreateUserListPacket;
    procedure 	sCreateFileListPacket;
    procedure 	BroadcastNewGroup;

    procedure 	sSaveFile(Name: Shortstring);
    function 	AddFile(var XPacket: TPacket): boolean;
    procedure	sRemoveFile(FileName: Shortstring);
    procedure 	KickOff;
    procedure 	SetGrpName(GName: ShortString);
    procedure 	SetMode(Server: boolean);
  public
    property	GrpName: Shortstring read FGrpName write SetGrpName;
    property  	IsServer: boolean read FIsServer write SetMode;
    constructor	CreateGrp(AOwner: TComponent;Name, Pass:string;S_Mode: boolean;S_Nick: String);
    procedure 	ReceiveMessage(var XPacket: TPacket);
  end;

var ChannelForm: TChannelForm;


implementation uses MainUnit, ErrorF, GroupsF, DirDlg, BigFiles, UserList;
{$R *.DFM}

{$I Channel1.pas}
{$I Channel2.pas}

constructor TChannelForm.CreateGrp(AOwner: TComponent;Name, Pass:string;S_Mode: boolean;S_Nick: String);
begin
  inherited Create(AOwner);
  IsServer:=S_Mode;
  ServerNick:=S_Nick;
  Password:=Pass;
  GrpName:=Name;
  SelfGP:=GrpName+CRLF+Password;
  ClientWidth:=255;
  ClientHeight:=150;
  Users:=TStringList.Create;
  Files:=TFileList.Create;	// server
  Msgs:=TStringList.Create;
  Packet:=TPacket.Create;
  Active:=true;
  Opt_Login:=false;Opt_Files:=false;Opt_Dnload:=false;
  if S_Mode then BroadcastNewGroup// pokud je to server, tak rozeslat msg
   else begin
    Packet.NewPacket(cmUserListReq, SelfGP);
    Packet.SendToUser(ServerNick);
    Packet.NewPacket(cmFileListReq, SelfGP);
    Packet.SendToUser(ServerNick);
   end;{else}
end;

procedure TChannelForm.SetGrpName(GName: ShortString);
begin
 Self.Caption:=GName{$IFDEF Debug}+' ('+Password+')'{$EndIf};
 Self.FGrpName:=GName;
end;

procedure TChannelForm.SetMode(Server: boolean);
begin
 FIsServer:=Server;
 // >>> remove servermenu if not FIsServer
end;

procedure TChannelForm.SetMessage(const Msg: string;Index: integer);
var I: integer;
begin
 if (Self.Msgs.Count > Index) then Self.Msgs[Index]:=Msg
  else begin
   if (Self.Msgs.Count < Index) then
     for I:=Self.Msgs.Count to (Index-1) do Self.Msgs.Add('?');
   Self.Msgs.Add(Msg);
  end;{if}
 for I:=0 to (Msgs.Count-1) do
  if Msgs[I] <> ChatBox.Lines[I] then ChatBox.Lines[I]:=Msgs[I];
 if (Msgs.Count > ChatBox.Lines.Count) then
  for I:=ChatBox.Lines.Count to (Msgs.Count-1) do
   ChatBox.Lines.Add(Msgs[I]);
end;

procedure TChannelForm.sCreateUserListPacket;
var I: integer;
begin
  Packet.NewPacket(smUserList, SelfGP);
  for I:=0 to (Users.Count-1) do Packet.Add(Users[I]);
end;

procedure TChannelForm.sCreateFileListPacket;
var I: integer;
begin
  Packet.NewPacket(smFileList, SelfGP);
  for I:=0 to (Files.Count-1) do
   if (Files[I] <> nil) then Packet.Add(Files[I].FileName);
end;

procedure TChannelForm.BroadcastNewGroup;
begin
 Packet.NewPacket(smGroupName, GrpName);
 GroupForm.ReceiveGroupName(Packet); // >>> supposed to be here ??
 Packet.Broadcast;
end;

procedure TChannelForm.ChatEditKeyPress(Sender: TObject; var Key: Char);
begin
 if Key = #13 then begin
   with ChatEdit do
     if (Items.IndexOf(Text) = -1) then Items.Add(Text);
   Packet.NewPacket(cmMsg, SelfGP+CRLF+'<'+LANCHUsers.LocalUser+'>'+ChatEdit.Text);
   if IsServer then sReceiveMessage(Packet)
     else Packet.SendToUser(ServerNick);
   Self.ChatEdit.SelectAll;
 end;{if}
end;

(*****************************************************************)
(*******************************************************************)
procedure TChannelForm.SaveChat(Sender: TObject);
begin
  MainForm.SaveDlg.FilterIndex:=1;
  MainForm.SaveDlg.FileName:=Self.GrpName+'.txt';
  if MainUnit.MainForm.SaveDlg.Execute then
    Self.ChatBox.Lines.SaveToFile(MainUnit.MainForm.SaveDlg.FileName);
end;

procedure TChannelForm.Death(Sender: TObject);
var Msg: ANSIstring;
begin
 case Self.IsServer of
  true: Msg:=LoadStr(STR_DestroyGrp);
  false:Msg:=LoadStr(STR_LogOut);
 end;{case}
 {$IFNDEF DEBUG}
 if (Sender <> MainForm) and (Windows.MessageBox(Self.Handle, PChar(Msg), PChar(Application.Title), MB_ICONWARNING or MB_YESNO or MB_DEFBUTTON2) <> IDYES) then EXIT;
//(MessageDlg(Msg, mtWarning, [mbYes, mbNo], 0) <> mrYes)
 {$ENDIF}
 if IsServer then	{ server }
  begin
   Packet.NewPacket(smKick, SelfGP);
   SendToUsers;
   Packet.NewPacket(amGroupKO, SelfGP);
   Packet.Broadcast;
{   GroupForm.Groups.Delete(GroupForm.Groups.IndexOf(Self.GrpName));GroupForm.FillList;}
  end
  else                 { client }
   if Active then begin
    Packet.NewPacket(cmLogout, SelfGP);
    Packet.SendToUser(ServerNick);
   end;
 Self.Free;
end;

procedure TChannelForm.ReceiveMessage(var XPacket: TPacket);
begin
 if IsServer and ({(XPacket.IDCode = amGroupNames) or} (XPacket.IDCode = cmLogin))
    then Self.SReceiveMessage(XPacket)
 else
 if (XPacket[1] <> GrpName) then Error(Self.GrpName+': prisel paket jiny skupiny')
 else
  if (XPacket[2] <> Self.Password) then Error(Self.GrpName+': prisel hackerskej paket')
  else
   if Self.IsServer then Self.sReceiveMessage(XPacket) else Self.cReceiveMessage(XPacket);
end;

procedure TChannelForm.SendToUsers;
var I: integer;
begin
 for I:=0 to (Self.Users.Count-1) do
  Packet.SendToUser(Users[I]);
end;

procedure TChannelForm.sReceiveMessage(var XPacket: TPacket);
var I, Index, Count: integer;
    P: PChar;
    S3: shortstring;
    Sh: ANSIString;
begin
 case XPacket.IDCode of
  cmLogIn: if not Opt_Login then begin { nekdo se chce lognout };
            for I:=0 to (Users.Count-1) do
             if (UpperCase(XPacket[2]) = UpperCase(PChar(Users.Objects[I]))) then begin
              Error(XPacket[2]+' ve skupinì již je');
              EXIT;
             end;{if}
            Packet.NewPacket(smLoginReply, GrpName);
            Sh:=XPacket.SenderN+' se chce lognout';
            case Windows.MessageBox(Self.Handle, PChar(Sh), PChar(Application.Title), MB_ICONQUESTION or MB_YESNOCANCEL) of
{IDYES}      IDYES: begin
              Packet.Add(Self.Password);
              P:=StrAlloc(Length(XPacket[2])+1);// copy to user list
              StrPCopy(P, XPacket[2]);
              Users.AddObject(XPacket[0], TObject(P));
             end;
{IDNO	     IDNO: ;}
{IDCANCEL}   IDCancel: RestrictClick(SMenuIgnoreLogin);
            end;{case}
            Packet.SendToUser(XPacket.SenderN);
{disabled} end else Error(XPacket[2]+ ' se chtel lognout');
  cmUserListReq: begin { client chce user list }
                sCreateUserlistPacket;
                Packet.SendToUser(XPacket.SenderN);
              end;
  cmMsgReq: begin { poslat stary zpravy }
              Index:=StrToInt(XPacket[3]);
              Count:=StrToInt(XPacket[4]);
              if (Index > Msgs.Count) then
		begin {$IFDEF DEBUG}BreakIf(true, 'user chce neexistujici zpravy');{$ENDIF}EXIT;end;
              if ((Count+Index) > Msgs.Count) then Count:=Msgs.Count-Index;
              Packet.NewPacket(smMsgList,SelfGP);
              Packet.Add(XPacket[3]);
              for I:=0 to (Count-1) do Packet.Add(Msgs[Index+I]);
               Packet.SendToUser(XPacket.SenderN);
            end;
  cmMsg:    begin { nova message; if IsServer -> Packet = XPacket }
              S3:=XPacket[3];
              SetMessage(S3, Msgs.Count);
              Packet.NewPacket(smMsgList,SelfGP);
              Packet.Add(IntToStr(Self.Msgs.Count-1));{ cislo zpravy }
              Packet.Add(S3);                         { obsah zpravy }
              Self.SendToUsers;
            end;
  cmLogout: begin{ nekdo to vzdal }
             Index:=Users.IndexOf(XPacket[0]);
             Error(PChar(Users.Objects[Index])+' ('+XPacket[0]+') vypadl z '+Self.GrpName);
             Users.Delete(Index);
             sCreateUserListPacket;SendToUsers;
             {$IFDEF DEBUG}ShowMessage(Self.GrpName+' user logged out');{$ENDIF}
            end;
  gmFileReq:if not Opt_Dnload then begin { nekdo chce soubor }
                I:=Files.IndexOf(XPacket[3]);
                if ((I <> -1) and ((Files[I].Status and stComplete) = stComplete)) then
                 try
                   Files[I].Send(SelfGP, XPacket.SenderN, gmFile);
                 except
                  CriticalError(GrpName+': chyba pri odesilani '+XPacket[3]);
                 end{try/e}
                else Error(GrpName+': soubor '+XPacket[3]+' nelze odeslat')
{disabled}    end else Error(XPacket[0]+ ' chtel '+ XPacket[3]);
  gmFile: if not Opt_Files then begin
              AddFile(XPacket);
              if (StrToInt(XPacket[5]) = -1) then
                begin sCreateFilelistPacket;SendToUsers;end;
{disabled}   end else Error(XPacket[0]+' chtel poslat ' +XPacket[3]);
  cmFileListReq: begin { nekdo chce seznam souboru }
                   sCreateFilelistPacket;
                   Packet.SendToUser(XPacket.SenderN);
                 end;
 end; {case}
end;

procedure TChannelForm.CReceiveMessage(var XPacket: TPacket);
var I, S: integer;
begin
 case XPacket.IDCode of
  smKick: begin
           {$IFDEF DEBUG}Error(Self.GrpName+' User kicked');{$ENDIF}
           ShowMessage(Self.GrpName+': Bye bye !');
           Self.Active:=false;
           Self.ChatEdit.Enabled:=false;
          end;
  smUserList: begin{seznam useru }
               Self.Users.Clear;
               for I:=2 to (XPacket.Count-1) do Self.Users.Add(XPacket[I]);
               {$IFDEF DEBUG}Error(Self.GrpName+': Updated user list');{$ENDIF}
              end;
  smFileList: begin{ seznam souboru }
               for I:=(Files.Count-1) downto{!} 0 do
                if ((Files[I].Status and stRemote) = stRemote) then
                  Files.Delete(I);
               for I:=2 to (XPacket.Count-1) do
                if (Files.IndexOf(XPacket[I]) = -1) then
                  Files.Add(TFile.CreateRemote(XPacket[I]));
               {$IFDEF DEBUG}Error(Self.GrpName+': Updated file list');{$ENDIF}
              end;
  smMsgList:  begin{ zprava }
               S:=StrToInt(XPacket[2]);
               if (Msgs.Count < S) then begin{ chybi najaka starsi zprava }
                 Packet.NewPacket(cmMsgReq, SelfGP);
                 Packet.Add(IntToStr(Msgs.Count));
                 Packet.Add(IntToStr(S - Msgs.Count));
                 Packet.SendToUser(ServerNick);
               end;{if}
               for I:=3 to (XPacket.Count-1) do
                  SetMessage(XPacket[I], S+I-3);
              end;
  gmFile: //begin
           if AddFile(XPacket) then begin
            I:=Files.IndexOf(XPacket[3]);
{$IFDEF DEBUG}if I = -1 then raise Exception.Create('Chyba !!!!!!!!!');{$ENDIF}
            if not (((Files[I].Status and stInvalidCRC) <> 0) and (Windows.MessageBox(Self.Handle,'Uložit soubor, i když má špatné CRC ?','LANCHmeAT', MB_ICONSTOP or MB_YESNO) <> IDYES)) then
               begin
                  Files[I].Save;
                  Files.Delete(I);
                  Files.Add(TFile.CreateRemote(XPacket[3]));
               end;
           end;
 end;{case}
end;


procedure TChannelForm.KickOff; // >>> predelat
var I: integer;
begin
 {$IFDEF DEBUG}BreakIf(not IsServer,'!!!');{$ENDIF}
  if (Windows.MessageBox(Self.Handle, PChar('Odhlásit '+ANSIString(Users[I])+' ?'), PChar(Application.Title), MB_ICONQUESTION or MB_YESNO or MB_DEFBUTTON2) = IDYES) then begin
   Packet.NewPacket(smKick, SelfGP);
   Packet.SendToUser(Users[I]);
   Error('A má to za sebou, hajzl');
   Self.Users.Delete(I);
  end;{if} 
end;

procedure TChannelForm.FormClose(Sender: TObject;var Action: TCloseAction);
begin
 Action:=caNone;
 Self.Death(Sender);
end;

procedure TChannelForm.RestrictClick(Sender: TObject);
begin
{$IFDEF DEBUG}if not IsServer then showmessage('!!!');{$ENDIF}
 if (Sender = SMenuIgnoreLogin) then Opt_Login:=not Opt_Login
 else
  if (Sender = SMenuIgnoreFiles) then Opt_Files:=not Opt_Files
  else
   if (Sender = SMenuIgnoreDnlds) then Opt_Dnload:=not Opt_Dnload;
 SMenuIgnoreLogin.Checked:=Opt_Login;
 SMenuIgnoreFiles.Checked:=Opt_Files;
 SMenuIgnoreDnlds.Checked:=Opt_Dnload;
end;

procedure TChannelForm.ChatBoxKeyPress(Sender: TObject; var Key: Char);
begin
 ChatEdit.SetFocus;
{ ChatEdit.Text:=ChatEdit.Text+Key;}
end;

(**************************************************************)

procedure TChannelForm.SendDir(Sender: TObject);
var Dir: Shortstring;
    F: TFile;
    I: integer;
begin
  Dir:=BrowseDirectoryMP({'c:\', }'Zvolte adresáø');
  if (Dir = '') then EXIT;
//  CriticalError(Dir);
  try
    F:=TFile.LoadDir(Dir);
  except
    CriticalError(GrpName+': nepovedlo se naèíst adresáø');
    EXIT;
  end;{try/e}

  if IsServer then begin		// server
   I:=Files.IndexOf(Dir);
   if (I <> -1) then
    if (MessageDlg('Soubor jiz existuje, pøepsat ?', mtWarning, [mbYes, mbNo], 0) = mrYes) then
      begin
        Files.Delete(I);
        Files.Add(F);
      end{if}
    else F.Free
   else begin Files.Add(F);sCreateFilelistPacket;SendToUsers;end;
  end{if}
  else begin                         // client
   F.Send(SelfGP, ServerNick, gmFile);
  end;{else}
end;

end.

