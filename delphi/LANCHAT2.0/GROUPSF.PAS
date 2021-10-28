{$I _hdr.inc}

unit GroupsF;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, ExtCtrls, Menus, PackUnit;

type
  TGroupForm = class(TForm)
    ListBox1: 	TListBox;
    GroupsMenu: TPopupMenu;
    MenuRefresh: TMenuItem;
    procedure 	ListBox1DblClick(Sender: TObject);
    procedure 	Search(Sender: TObject);
    procedure 	FormCreate(Sender: TObject);
    procedure 	FormClose(Sender: TObject; var Action: TCloseAction);
    procedure 	ListBox1Click(Sender: TObject);
  private
    Packet:     TPacket;
    ActiveApp:	boolean;
    procedure	FillList;
  public
    Groups:   	TStringList;
    procedure 	ReceiveGroupName(XPacket: TPacket);{smGroupName}
    procedure 	ReceiveLoginReply(XPacket: TPacket);{smLoginReply}
    function	GroupExists(const Name: shortstring): boolean;
    procedure	RemoveGroup(Name: shortstring);
  end;

var GroupForm: TGroupForm;

implementation uses ChannelF, ErrorF, Tools, MainUnit, UserList;
{$R *.DFM}

type
 PServer = ^TServer;
 TServer = record
    Admin: Shortstring;
 end;

procedure TGroupForm.ListBox1DblClick(Sender: TObject);
var Grp: shortstring;
begin
{$IFDEF DEBUG} if (Self.ListBox1.ItemIndex = -1)then ShowMessage('It''s strange !');{$ENDIF}
  if (LANCHUsers.NickEmpty) then begin ShowMessage(LoadStr(STR_NoInfo));EXIT;end;
  Grp:=Self.ListBox1.Items[Self.ListBox1.ItemIndex];
  if MainUnit.MainForm.FindTarget(Grp) <> nil then
   begin ShowMessage(LoadStr(STR_AlreadyLogged));EXIT;end;
  Packet.NewPacket(cmLogIn,Grp);
  Packet.SendToUser(PServer(Groups.Objects[Groups.IndexOf(Grp)])^.Admin);
end;
           {  smLogInReply  }
procedure TGroupForm.ReceiveLoginReply(XPacket: TPacket);
begin
 {$IFDEF DEBUG}if XPacket.IDCode <> smLoginReply then ShowMessage('Chyba v ReceiveLoginReply !!!');{$ENDIF}
 if (XPacket.Count < 4) then ShowMessage('Smùla, vopruza jako seš ty '#13'tam zøejmì nechtìj')
  else
   if (MainForm.FindTarget(XPacket[1])<>nil) then
     ShowMessage(LoadStr(STR_AlreadyLogged))
   else
     TChannelForm.CreateGrp(MainForm, { owner }
       XPacket[1],	{ name }
       XPacket[3],	{ password }
       false,			{ IsServer }
       XPacket[2]);	{ admin's nick }
end;
              { smGroupName }
procedure TGroupForm.ReceiveGroupName(XPacket: TPacket);
var S: PServer;
begin
{$IFDEF DEBUG}BreakIf(XPacket.IDCode <> smGroupName,'Chyba v ReceiveGroupName !!!');{$ENDIF}
 if (not GroupExists(XPacket[1])) then begin
  New(S);// 0=sender computer / 1=group name / 2=admin's nick
  S^.Admin:=XPacket.SenderN;
  Self.Groups.AddObject(XPacket[0], TObject(S));
  Self.FillList;
 end;{if}
end;

procedure TGroupForm.FillList;
var I: integer;
begin
 ListBox1.Hint:='Seznam skupin';
 Self.ListBox1.Items.Clear;
 for I:=0 to (Groups.Count-1) do
  Self.ListBox1.Items.Add(Groups[I]);
end;

procedure TGroupForm.Search(Sender: TObject);
var I: integer;
    S: PServer;
    Frm: TChannelForm;
begin
  Packet.NewPacket(amGroupNames, '');
  Packet.Broadcast;
  Groups.Clear;       // smazat grupy a uzivatele
  LANCHUsers.WaitForRefresh;
//  if (PublicForm <> nil) then PublicForm.CopyUsersToMenu; >>>
  for I:=0 to (MainForm.MDIChildCount-1) do { snad bude fungovat tohle }
   if MainForm.MDIChildren[I] is TChannelForm then begin
    Frm:=TChannelForm(MainForm.MDIChildren[I]);
    if Frm.IsServer and (not GroupExists(Frm.GrpName)) then begin
     New(S);
     S^.Admin:=LANCHUsers.LocalUser;
     Self.Groups.AddObject(Frm.GrpName, TObject(S));
    end;{if}
   end;{if}
  Self.FillList;
end;

function TGroupForm.GroupExists(const Name: shortstring): boolean;
var I: integer;
    G: shortstring;
begin
 G:=UpperCase(Name);
 RESULT:=false;
 for I:=0 to (Groups.Count-1) do
  if (G = UpperCase(Groups[I])) then RESULT:=true;
end;

procedure TGroupForm.RemoveGroup(Name: shortstring);
var I: integer;
begin
 I:=Groups.IndexOf(Name);
 if (I = -1) then Error('Skupina neni v seznamu')
  else begin
   Dispose(PServer(Groups.Objects[I]));
   Groups.Delete(I);
   Self.FillList;
  end;{else}

end;

(*****************************************************************)
(*****************************************************************)
(*****************************************************************)

procedure TGroupForm.FormCreate(Sender: TObject);
begin
 ClientWidth:=80;
 ClientHeight:=112;
 Packet:=TPacket.Create;
 Groups:=TStringList.Create;
 Groups.Sorted:=true;
 Groups.Duplicates:=dupIgnore;
 ActiveApp:=true;
 {$IFDEF PTN}
  MenuBreak:=TMenuItem.create(Self);
  MenuBreak.Caption:='Stop';
  MenuBreak.Hint:='Aktivovat/deaktivovat LANCHmeAT';
  MenuBreak.OnClick:=MenuBreakClick;
  GroupsMenu.Items.Add(MenuBreak);
 {$ENDIF}
{ ListBox1DblClick(Sender);}
end;

procedure TGroupForm.FormClose(Sender: TObject; var Action: TCloseAction);
begin
 Action:=caMinimize;
end;

{$IFDEF PTN}
const
 ActiveAppStr: array[false..true] of string[5]=('Start','Stop');
procedure TGroupForm.MenuBreakClick(Sender: TObject);
begin
 ActiveApp:=not ActiveApp;
 MenuBreak.Caption:=ActiveAppStr[ActiveApp];
 MainForm.Timer1.Enabled:=ActiveApp;
end;
{$ENDIF}

procedure TGroupForm.ListBox1Click(Sender: TObject);
var I: integer;
begin
 I:=Groups.IndexOf(ListBox1.Items[ListBox1.itemindex]);
 if (I <> -1) then
 ListBox1.Hint:=Groups[I]+': '+PServer(Groups.Objects[I])^.Admin;
end;

end.

