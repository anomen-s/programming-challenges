{$I _hdr.inc}
unit PublicF;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, Menus,
  UserList, PackUnit;

type
  TPublicForm = class(TForm)
    ChatBox: 	TMemo;
    ChatEdit: 	TComboBox;
    PublicMenu: TPopupMenu;
    MenuSave: 	TMenuItem;
    MenuClear: 	TMenuItem;
    MenuN1: 	TMenuItem;
    procedure 	FormResize(Sender: TObject);
    procedure	FormCreate(Sender: TObject);
    procedure 	ChatEditKeyPress(Sender: TObject; var Key: Char);
    procedure 	FormClose(Sender: TObject; var Action: TCloseAction);
    procedure 	SaveChat(Sender: TObject);
    procedure 	ChatBoxKeyPress(Sender: TObject; var Key: Char);
    procedure 	MenuClearClick(Sender: TObject);
    procedure	MenuUserClick(Sender: TObject);
  public
    procedure	CopyUsersToMenu;
    procedure   ReceiveMsg(Msg: Shortstring);
  private
    Packet:	TPacket;
    OldMsg:	ShortString;
  end;


var
 PublicForm: TPublicForm;


implementation uses MainUnit, Tools;
{$R *.DFM}

const MENU_ITEMS = 3;

procedure TPublicForm.ReceiveMsg(Msg: ShortString);
begin
 Self.ChatBox.Lines.Add(Msg);
end;

procedure TPublicForm.ChatEditKeyPress(Sender: TObject; var Key: Char);
var Msg: ShortString;
begin
 if (Key = #13) and (ChatEdit.Text <> '') and (not LANCHUsers.NickEmpty) then begin
  Msg:='<'+LANCHUsers.LocalUser+'>'+ChatEdit.Text;
  ChatEdit.SelectAll;
  with ChatEdit do if (Items.IndexOf(Text) = -1) then Items.Add(Text);
  if (Msg <> OldMsg) then begin // zakazano posilani stejnych zprav
    Packet.Empty;
    Packet.Text:=Msg;
    Packet.IDCode:=amPublicMsg;
    Packet.Broadcast;
    OldMsg:=Msg;
  end;{if}
 end;{if}
end;

procedure TPublicForm.ChatBoxKeyPress(Sender: TObject; var Key: Char);
begin
 if ChatEdit.Enabled then ChatEdit.SetFocus;
end;

procedure TPublicForm.MenuClearClick(Sender: TObject);
begin
 if (Windows.MessageBox(Self.Handle, PChar(LoadStr(STR_ClearChat)), PChar(Application.Title), MB_ICONWARNING or MB_YESNO or MB_DEFBUTTON2) = IDYES) then
               { >>> zobrazuje se blbej hint }
// if MessageDlg(LoadStr(STR_ClearChat), mtWarning, [mbYes, mbNo], 0) = mrYes then
   Self.ChatBox.Lines.Clear
end;

procedure TPublicForm.SaveChat(Sender: TObject);
begin
  MainForm.SaveDlg.FileName:='verejny.txt';
  MainForm.SaveDlg.Filter:=LoadStr(STR_TXTFiles);
  if MainUnit.MainForm.SaveDlg.Execute then
    Self.ChatBox.Lines.SaveToFile(MainUnit.MainForm.SaveDlg.FileName);
end;

procedure TPublicForm.CopyUsersToMenu;
var User: TMenuItem;
    I: integer;
    r: PUserInfo;
begin
 if (not LANCHUsers.Changed) then EXIT;
 for I:=(PublicMenu.Items.Count-1) downto (LANCHUsers.Count+MENU_ITEMS) do begin
   User:=PublicMenu.Items[I];
   PublicMenu.Items.Delete(I);
   User.Free;
 end;{for}
            	{ nastavit jmena }
 for I:=MENU_ITEMS to (PublicMenu.Items.Count-1) do begin
   r:=LANCHUsers[I-MENU_ITEMS];
   PublicMenu.Items[I].Caption:=r^.UserName;
   PublicMenu.Items[I].Tag:=(I-MENU_ITEMS);
   PublicMenu.Items[I].Hint:=LoadStr(STR_SendPrivate)+r^.Computer;
 end;{for}
		{ pridat nove TMenuItems }
 for I:=(PublicMenu.Items.Count-MENU_ITEMS) to (LANCHUsers.Count-1) do begin
  r:=LANCHUsers[I];
  User:=TMenuItem.Create(Self);
  User.Caption:=r^.UserName;
  User.Tag:=I;
  User.Hint:=LoadStr(STR_SendPrivate)+r^.Computer;
  User.OnClick:=MenuUserClick;
  PublicMenu.Items.Add(User);
 end;{for}
end;

procedure TPublicForm.MenuUserClick(Sender: TObject);
var PMsg: ANSIstring;
    r: PUserInfo;
begin
 {$IFDEF DEBUG}if (not (Sender is TMenuItem)) then ShowMessage('Chyba v MenuUserClick'); {$ENDIF}
 r:=LANCHUsers.Items[(Sender as TMenuItem).Tag];
 if (not LANCHUsers.NickEmpty) then
  if (r^.UserStatus = uLocal) then
   ShowMessage('Ty jsi ale debil.'#13'Proè posíláš zprávu sám sobì?');
  if (InputQuery('Zpráva pro '+r^.UserName, 'Zadejte text zprávy:', PMsg)) and (PMsg <> '') then
   begin
    ReceiveMsg('['+r^.UserName+']'+PMsg);
    Packet.NewPacket(amPublicMsg, LANCHUsers.LocalUser+': '+PMsg);
    Packet.SendToUser(r^.UserName);
   end;{if}
end;

(**************************************************************)
(**************************************************************)
(**************************************************************)

procedure TPublicForm.FormCreate(Sender: TObject);
begin
 ClientHeight:=198;
 ClientWidth:=182;
 Packet:=TPacket.Create;
 CopyUsersToMenu;
end;


procedure TPublicForm.FormResize(Sender: TObject);
var X, Y: integer;
begin
 X:=ClientWidth;Y:=ClientHeight;
 ChatEdit.Width:=X-4;
 ChatEdit.Top:=Y-24;
 ChatBox.Height:=Y-32;
end;

procedure TPublicForm.FormClose(Sender: TObject; var Action: TCloseAction);
begin
 if (Windows.MessageBox(Self.Handle, PChar(LoadStr(STR_AskStop)), PChar(Application.Title), MB_ICONWARNING or MB_YESNO or MB_DEFBUTTON2) = IDYES) then begin
// if MessageDlg(LoadStr(STR_AskStop), mtWarning, [mbYes, mbNo], 0) = mrYes then begin
  PublicForm:=nil;
  {Self.Free;}
  Action:=caFree;
 end{if}
 else Action:=caNone;
end;

end.

