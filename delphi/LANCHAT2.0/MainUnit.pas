{$I _hdr.inc}

{>>> predelat Dialogs.MessageDlg na Windows.MessageBox }
unit MainUnit;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls,
  Forms, Dialogs, Menus, ExtCtrls, ComCtrls, StdCtrls,
  FileList, ChannelF, PackUnit, Tools;

type
  TMainForm = class(TForm)
    Timer1: 	TTimer;
    SaveDlg:	TSaveDialog;
    OpenDlg: 	TOpenDialog;
    StatusBar: 	TStatusBar;
    MainMenu: 	TMainMenu;

    MMenuComm:  TMenuItem;  	// menu Rozhovor
    MenuCreate: TMenuItem;
    MenuN1:  	TMenuItem;
    MenuUserInfo:TMenuItem;
    MenuN2: 	TMenuItem;
    MenuExit:	TMenuItem;
    MMenuWins:	TMenuItem;  	// Menu Okna
    WMenuTileHoriz: TMenuItem;
    WMenuCascade: TMenuItem;
    WMenuTileVert: TMenuItem;
    WMenuMin: 	TMenuItem;
    WMenuRestore: TMenuItem;
    MenuNw: 	TMenuItem;
    WMenuStatus:TMenuItem;
    WMenuGroups:TMenuItem;
    WMenuPublic:TMenuItem;
    MMenuHelp:	TMenuItem;	// Menu Nápovìda
    MenuHelp:   TMenuItem;
    MenuAbout:	TMenuItem;
    procedure	MenuAboutClick(Sender: TObject); // menu events
    procedure   MenuExitClick(Sender: TObject);
    procedure	MenuCreateClick(Sender: TObject);
    procedure	MenuUserInfoClick(Sender: TObject);
    procedure	MenuTileHorizVertClick(Sender: TObject);
    procedure	WMenuCascadeClick(Sender: TObject);
    procedure   MenuTileHorizClick(Sender: TObject);
    procedure   WMenuMinClick(Sender: TObject);
    procedure 	WMenuRestoreClick(Sender: TObject);
    procedure 	WMenuStatusClick(Sender: TObject);
    procedure 	WMenuGroupsClick(Sender: TObject);
    procedure 	MenuHelpClick(Sender: TObject);
    procedure 	WMenuPublicClick(Sender: TObject);

    procedure	FormCreate(Sender: TObject); // form events
    procedure 	FormClose(Sender: TObject; var Action: TCloseAction);
    procedure 	FormResize(Sender: TObject);
    procedure   WriteHint(Sender: TObject);
//  procedure 	AppActivate(Sender: TObject);

    procedure   Timer1Timer(Sender: TObject); // timer events
    procedure 	Timer0Timer(Sender: TObject);

    function	FindTarget(Name: ShortString): TChannelForm;
    procedure	SendGroupNames;
   private
    Packet:	TPacket;
    StayOnTop:	boolean;
    SysMenu: 	HMenu;
    procedure 	SysCommand(var Msg: TMessage); message wm_SysCommand;
   public
    SFiles:	TList;
  end;

var MainForm: TMainForm;
    ChatWallPaper: TBitmap;

implementation uses About, InfoF,  ErrorF, GroupsF, PublicF, BigFiles, UserList;
{$R *.DFM}

procedure TMainForm.MenuAboutClick(Sender: TObject);
begin
 About.AboutBox.ShowModal;
end;

procedure TMainForm.MenuExitClick(Sender: TObject);
begin
 Close;
end;

procedure TMainForm.MenuCreateClick(Sender: TObject);
var GrpName: ANSIstring;
    I, Count: integer;
begin
 Count:=0; { "omezeni" poctu skupin }
 for I:=0 to (MDIChildCount-1) do
  if (MDIChildren[I] is TChannelForm) and TChannelForm(MDIChildren[I]).IsServer then Inc(Count);
 if (Count >= GroupsLimit) and
  (MessageDlg('Nejseš trochu moc ukecanej ?', mtConfirmation, [mbYes], 0) = mrYes)
    then EXIT;                                 // tohle se mi povedlo :-)
 {$IFNDEF DEBUG}
 if LANCHUsers.NickEmpty then ShowMessage(LoadStr(STR_NoInfo))
 else{$ENDIF}
  if (InputQuery(Application.Title, LoadStr(STR_EnterGrpName), GrpName)) and (GrpName <> '') then
    if (GroupForm.GroupExists(GrpName)) then ShowMessage(LoadStr(Str_GroupExists))
    else TChannelForm.CreateGrp(Self, GrpName, RandomName(PassLen), true, LANCHUsers.LocalUser);
end;

procedure TMainForm.SysCommand(var Msg: TMessage);
var FormPos, MFlags: integer;
begin
//if (Msg.WParam = sc_close) then begin OnClose:=nil;Halt(1);end;
  inherited;
  if (Msg.wParam = 666) then begin
   StayOnTop:=not StayOnTop;
   if StayOnTop then FormPos:=HWND_TOPMOST else FormPos:=HWND_NOTOPMOST;
   if StayOnTop then MFlags:=mf_checked else MFlags:=mf_unchecked;
   ModifyMenu(SysMenu, 666, mf_ByCommand or MFlags, 666, '&Stay on top');
   SetWindowPos(Self.Handle, FormPos, 0, 0, 0, 0, SWP_NOACTIVATE or SWP_NOMOVE or SWP_NOSIZE);
  end;{end}
end;

procedure TMainForm.FormCreate(Sender: TObject);
begin
 Randomize;
 SysMenu := GetSystemMenu(Handle, False);
 ModifyMenu(SysMenu, sc_Close, mf_ByCommand, sc_Close, '&Bye, bye!'#9'Alt+F4');
 AppendMenu(SysMenu, mf_Separator, 0, #0);
 AppendMenu(SysMenu, mf_ByCommand or mf_unchecked, 666, '&Stay on top');

 Self.Caption:=Application.Title;
 Application.OnHint:=Self.WriteHint;
 TileMode:=tbVertical;
 Packet:=TPacket.Create;
 SFiles:=TList.Create;
 Packet.NewPacket(amGroupNames,'');
 Packet.Broadcast;
 Packet.NewPacket(amUser, '+');
 Packet.Broadcast;
end;

procedure TMainForm.MenuUserInfoClick(Sender: TObject);
var I: integer;
    Active: boolean;
//  OldNick: shortstring;
begin
 Active:=false;
 for I:=0 to (Self.MDIChildCount-1) do
   if (Self.MDIChildren[I] is TChannelForm) then begin Active:=true;BREAK;end;
 InfoForm.ReadOnly:=Active; // pokud neni zadna skupina tak je moznost zmeny udaju
//OldNick:=UserData.Nick;
 if InfoForm.Execute and (InfoForm.OldNick <> '') then begin
   Packet.NewPacket(amUser, '-');
   Packet.Broadcast;
 end;
 if (not LANCHUsers.NickEmpty) then begin
   GroupForm.Search(Sender);
   MenuUserInfo.Default:=false;MenuCreate.Default:=true;
   Packet.NewPacket(amUser, '+');
   Packet.Broadcast;
   Timer1.OnTimer:=Timer1Timer;
 end;{if}
end;

procedure TMainForm.MenuTileHorizVertClick(Sender: TObject);
begin Self.TileMode:=tbVertical;Self.Tile;end;

procedure TMainForm.MenuTileHorizClick(Sender: TObject);
begin Self.TileMode:=tbHorizontal; Self.Tile;end;

procedure TMainForm.WMenuCascadeClick(Sender: TObject);
begin Self.Cascade;end;

procedure TMainForm.WMenuMinClick(Sender: TObject);
var I: integer;
begin
  for I:= (Self.MDIChildCount-1) downto 0 do Self.MDIChildren[I].WindowState := wsMinimized;
end;

procedure TMainForm.WMenuRestoreClick(Sender: TObject);
var I: integer;
begin
  for I:= 0 to (Self.MDIChildCount-1) do Self.MDIChildren[I].WindowState := wsNormal;
end;

procedure TMainForm.WMenuStatusClick(Sender: TObject);
begin
 if (ErrorForm <> nil) then ErrorForm.WindowState:=wsNormal
   else ErrorForm:=TErrorForm.Create(Self);
 ErrorForm.BringToFront;
end;

procedure TMainForm.WMenuGroupsClick(Sender: TObject);
begin
 GroupForm.WindowState:=wsNormal;GroupForm.BringToFront;
end;

procedure TMainForm.WMenuPublicClick(Sender: TObject);
begin
 if (PublicForm <> nil) then PublicForm.WindowState:=wsNormal
  else PublicForm:=TPublicForm.Create(Self);
 PublicForm.BringToFront;
end;

procedure TMainForm.MenuHelpClick(Sender: TObject);
begin
 ShowMessage('Nápovìda není k dispozici'+#13+'(a ani jen tak nebude)');
end;

(*procedure TMainForm.AppActivate(Sender: TObject);
begin
 Application.Restore;
end;*)

procedure TMainForm.WriteHint(Sender: TObject);
begin
 Self.StatusBar.Panels[0].Text:=Application.Hint;
end;

function TMainForm.FindTarget(Name: ShortString): TChannelForm;
var I: integer;
begin
 for I:=0 to (Self.MDIChildCount-1) do
  if (Self.MDIChildren[I] is TChannelForm) and
     (UpperCase(Name) = UpperCase((Self.MDIChildren[I] as TChannelForm).GrpName)) then
       begin
        RESULT:=TChannelForm(Self.MDIChildren[I]);
        EXIT;
       end;{if}
 RESULT:=nil;
end;

procedure TMainForm.SendGroupNames;
var I: integer;
begin
 { tohle vypada OK }
 Packet.NewPacket(amUser, '');
 Packet.SendToUser(Packet.SenderN);
 for I:=0 to (Self.MDIChildCount-1) do
  if (Self.MDIChildren[I] is TChannelForm) and
      (Self.MDIChildren[I] as TChannelForm).IsServer then begin
    Packet.NewPacket(smGroupName, TChannelForm(Self.MDIChildren[I]).GrpName);
    Packet.SendToUser(Packet.SenderN);
  end;{if}
end;

procedure TMainForm.FormClose(Sender: TObject; var Action: TCloseAction);
var I: integer;
begin
{$IFNDEF DEBUG}
 for I:=0 to (Self.MDIChildCount-1) do
   if (Self.MDIChildren[I] is TChannelForm) then
    begin Action:=caNone;ShowMessage(LoadStr(STR_ForceClose));EXIT;end;
// if MessageDlg(LoadStr(STR_AskClose), mtConfirmation, [mbYes, mbNo], 0) = mrYes then begin
 if Windows.MessageBox(Self.Handle,PChar(LoadStr(STR_AskClose)), PChar(Application.Title), MB_ICONQUESTION or MB_YESNO or MB_DEFBUTTON2) = IDYES then begin
{$ENDIF}
  for I:=0 to (Self.MDIChildCount-1) do
   if (Self.MDIChildren[I] is TChannelForm) then
     (Self.MDIChildren[I] as TChannelForm).Death(Self);

  if (not LANCHUsers.NickEmpty) then begin
   Packet.NewPacket(amUserKO, '');
   Packet.Broadcast;
  end;{if}

  Action:=caFree;
{$IFNDEF DEBUG}
 end{if}
 else Action:=caNone;
{$ENDIF}
end;

{)))))))))))))))))))))))))))))))))))))))))))))))))))))}

procedure TMainForm.Timer0Timer(Sender: TObject);
begin
try
 if (IsNewMessage and ReceiveMessage(Packet)) then
   case Packet.IDCode of
    smGroupName:GroupForm.ReceiveGroupName(Packet);
    amGroupKO:  GroupForm.RemoveGroup(Packet[1]);
    amPublicMsg:if (PublicForm <> nil) then PublicForm.ReceiveMsg(Packet[0]);
    amUser:     LANCHUsers.ReceiveUser(Packet);
    amUserKO: 	LANCHUsers.DeleteUser(Packet);
   end;{case}
except
 ShowMessage('Chyba pøi pøijímání paketu');
end;{try/e}
 Packet.Empty;
end;

procedure TMainForm.Timer1Timer(Sender: TObject);
var Target: TChannelForm;
begin
 Self.Timer1.Enabled:=false;
try
 if (IsNewMessage and ReceiveMessage(Packet)) then
   case Packet.IDCode of
    cmMsg, cmMsgReq, cmLogout, cmLogIn, cmUserListReq,
    cmFileListReq, gmFile, gmFileReq,
    smMsgList, smKick, smUserList, smFileList:
    begin
     Target:=FindTarget(Packet[1]);
     if (Target = nil) then Error('Prijemce neexistuje')
       else Target.ReceiveMessage(Packet);
    end;
                  { add server name to list }
    smGroupName:  GroupForm.ReceiveGroupName(Packet);

    smLogInReply: GroupForm.ReceiveLoginReply(Packet);

    amGroupNames: SendGroupNames;

    amGroupKO:    GroupForm.RemoveGroup(Packet[1]);

    amPublicMsg:  if (PublicForm <> nil) then PublicForm.ReceiveMsg(Packet[0]);

    amUser:       LANCHUsers.ReceiveUser(Packet);

    amUserKO:     LANCHUsers.DeleteUser(Packet);
    else Error('Neznámý paket'+IntToHex(Packet.IDCode and $FF, 2));
   end;{case}
except
 ShowMessage('Nejaka chyba pri zpracovani paketu');
end;{try/e}
 Packet.Empty;
 if IsNewMessage then Timer1.Interval:=SHORT_PERIOD else Timer1.Interval:=LONG_PERIOD;
 Self.Timer1.Enabled:=true;
end;

procedure TMainForm.FormResize(Sender: TObject);
begin
 StatusBar.Panels[0].Width:=ClientWidth-48;
end;

initialization
 ChatWallPaper:=TBitmap.Create;
 ChatWallPaper.LoadFromResourceID(HInstance, 4);
 Application.Title:=Application.Title
 		{$IFDEF LocalDEBUG}+' * LOCAL'{$ENDIF}
                {$IFDEF DEBUG}+' * DEBUG'{$ENDIF}
                {$IFDEF BUG}+' * BUG'{$ENDIF}
                {$IFDEF DEBUGGER}+' * debugger'{$ENDIF};
end.

