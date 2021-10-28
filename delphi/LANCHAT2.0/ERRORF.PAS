{$I _hdr.inc}

unit ErrorF;

interface uses  Windows, Messages, SysUtils, Classes, Graphics,
                Controls, Forms, Dialogs, StdCtrls, Menus;

type
  TErrorForm = class(TForm)
    ErrorBox: 	TListBox;
    PopupMenu1: TPopupMenu;
    MenuClear: 	TMenuItem;
    MenuClose: 	TMenuItem;
    procedure 	FormCreate(Sender: TObject);
    procedure 	FormClose(Sender: TObject; var Action: TCloseAction);
    procedure 	MenuClearClick(Sender: TObject);
    procedure 	MenuCloseClick(Sender: TObject);
  end;

procedure Error(Str: shortstring);
procedure CriticalError(Str: shortstring);
procedure ErrorListClear;

var ErrorForm: TErrorForm;

implementation uses MainUnit{$IFDEF DEBUG},Debug{$ENDIF};
{$R *.DFM}

var _ErrorList: TStringList;

procedure Error(Str: shortstring);
begin
 _ErrorList.Add(Str);
 MainForm.StatusBar.Panels[1].Text:=IntToStr(_ErrorList.Count);
 if (ErrorForm <> nil) then
   ErrorForm.ErrorBox.Items.Assign(_ErrorList);
end;

procedure CriticalError(Str: shortstring);
begin
 {$IFDEF DEBUG}BreakIf(true, 'Crit. Error: '+Str);{$ENDIF}
 _ErrorList.Add(Str);
 MainForm.StatusBar.Panels[1].Text:=IntToStr(_ErrorList.Count);
 if (ErrorForm <> nil) then ErrorForm.WindowState:=wsNormal
   else ErrorForm:=TErrorForm.Create(MainForm);
 ErrorForm.ErrorBox.Items.Assign(_ErrorList);
 ErrorForm.BringToFront;
end;

procedure ErrorListClear;
begin
 if (ErrorForm <> nil) then
   ErrorForm.ErrorBox.Items.Clear;
 _ErrorList.Clear;
 MainForm.StatusBar.Panels[1].Text:='';
end;

procedure TErrorForm.FormCreate(Sender: TObject);
begin
 Self.CLientWidth:=150;
 Self.ClientHeight:=200;
{$IFNDEF DEBUG}
 Self.WindowState:=wsMinimized;
{$ENDIF}
 ErrorBox.Items.Assign(_ErrorList);
end;

procedure TErrorForm.FormClose(Sender: TObject; var Action: TCloseAction);
begin
 Action:=caMinimize;
end;

procedure TErrorForm.MenuClearClick(Sender: TObject);
begin
 ErrorListClear;
end;

procedure TErrorForm.MenuCloseClick(Sender: TObject);
begin
 ErrorForm:=nil;
 Self.Free;
end;

initialization
 _ErrorList:=TStringList.Create;

finalization
 _ErrorList.Free;
end.

