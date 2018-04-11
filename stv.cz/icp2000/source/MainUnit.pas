{$I hdr.inc}
unit MainUnit;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms,
  Dialogs, ComCtrls, ToolWin, StdCtrls, ExtCtrls, Menus,
  docunit;

type
  TMainForm = class(TForm)
    MainMenu1:  TMainMenu; // Menu File
    MMenuFile:  TMenuItem;
    MenuView:   TMenuItem;
    MenuReload: TMenuItem;
    MenuOpen:   TMenuItem;
    MenuSettings:TMenuItem;
    MenuN1:     TMenuItem;
    MenuExit:   TMenuItem;
    MMenuGo:    TMenuItem; // Menu Go
    MenuBack:   TMenuItem;
    MenuForward:TMenuItem;
    MenuN2:     TMenuItem;
    MMenuHelp:  TMenuItem; // Menu Help
    MenuAboutPrg:TMenuItem;
    MenuHelp: 	TMenuItem;
    MenuAbout:  TMenuItem;
    CoolBar1:   TCoolBar; // Coolbar
    ToolBar1:   TToolBar;
    OpenBtn:	TToolButton;
    ToolBtn2:	TToolButton;
    LeftButton: TToolButton;
    RightButton:TToolButton;
    ToolBtn4:	TToolButton;
    ReloadButton:TToolButton;
    ToolBtn5:	TToolButton;
    AboutButton:TToolButton;
    NormalImgs: TImageList;
    HotImgs:	TImageList;
    LocationEdit:TComboBox;
    StatusBar1: TStatusBar; // Status bar
    OpenDialog1:TOpenDialog;
    ScrollBar1: TScrollBar;
    procedure   FormResize(Sender: TObject);
    procedure 	ShowAbout(Sender: TObject);
    procedure 	FormCreate(Sender: TObject);
    procedure 	MenuOpenClick(Sender: TObject);
    procedure 	MenuViewClick(Sender: TObject);
    procedure 	MenuExitClick(Sender: TObject);
    procedure 	MenuSettingsClick(Sender: TObject);
    procedure 	LeftButtonClick(Sender: TObject);
    procedure 	RightButtonClick(Sender: TObject);
    procedure 	ReloadButtonClick(Sender: TObject);
    procedure	MenuGoClick(Sender: TObject);
    procedure 	ScrollBar1Change(Sender: TObject);
    procedure 	FormPaint(Sender: TObject);
    procedure 	MenuHelpClick(Sender: TObject);
    procedure 	CoolBar1Resize(Sender: TObject);
    procedure 	LocationEditKeyPress(Sender: TObject;var Key: Char);
    procedure 	FormMouseMove(Sender: TObject; Shift: TShiftState;X, Y: Integer);
    procedure 	FormClick(Sender: TObject);
    procedure 	FormClose(Sender: TObject;var Action: TCloseAction);
    procedure 	ScrollBar1KeyDown(Sender: TObject; var Key: Word;Shift: TShiftState);
  private
    Document:	TDocument;
    DocHistory:	TStringList;
    HistoryIndex:integer;
    TopY:	integer;
    CurrLink:	shortstring;
    function 	OpenDocument(const FileName: ANSIString): boolean;
    procedure	SetThreadData;
    procedure   SetButtons;
    procedure	HistoryToMenu;
    procedure	AddToHistory(FileName: ANSIString);
    function	IsLink(x, y: integer;var S: ShortString): boolean;
    procedure   ShowHint(Sender: TObject);
  end;

var  MainForm: TMainForm;

resourcestring
 AppName = 'SML Viewer'
   {$IFDEF DEBUGINFO}+' - DEBUG'{$IFNDEF DEBUG}+'INFO'{$ENDIF}{$ENDIF};

implementation uses about, fstream, config, display;
{$R *.DFM}

const GoIndex = 3; // number of items in 'Go' menu without history list

procedure TMainForm.SetButtons;
var B: boolean;
    I: integer;
begin
 B:=(HistoryIndex > 0);
 if (LeftButton.Down=B) then LeftButton.Down:=not B;
 if (LeftButton.Enabled<>B) then LeftButton.Enabled:=B;
 B:=(HistoryIndex < (DocHistory.Count-1));
 if (RightButton.Down = B) then RightButton.Down:=not B;
 if (RightButton.Enabled<>B) then RightButton.Enabled:=B;
 for I:=0 to (MMenuGo.Count-1) do
  MMenuGo.Items[I].Checked:=false;
 MMenuGo.Items[HistoryIndex+GOINDEX].Checked:=true;
end;

procedure TMainForm.FormResize(Sender: TObject);
begin
 ScrollBar1.Height:=ClientHeight-CoolBar1.Height-StatusBar1.Height;
 ScrollBar1.Left:=ClientWidth-ScrollBar1.Width;
 SetThreadData;
end;

procedure TMainForm.CoolBar1Resize(Sender: TObject);
begin
 ScrollBar1.Top:=CoolBar1.Height;
 SetThreadData;
 ScrollBar1.Height:=TCtrl.Height;
end;

procedure TMainForm.ShowAbout(Sender: TObject);
begin
 with TAboutForm.Create(Self) do
 try
  ShowModal;
 finally
  Free;
 end;{try/f}
end;

procedure TMainForm.SetThreadData;
begin
 TCtrl.Width:=ClientWidth-ScrollBar1.Width-2;
 TCtrl.Height:=ClientHeight-CoolBar1.Height-StatusBar1.Height;
 TCtrl.Top:=CoolBar1.Height;
 TCtrl.Left:=2;
 TCtrl.YPos:=Self.TopY;
 TCtrl.DoRepaint:=true;
end;

procedure TMainForm.ShowHint(Sender: TObject);
begin
 StatusBar1.SimpleText:=Application.Hint;
end;

procedure TMainForm.FormCreate(Sender: TObject);
var P: ANSIString;
begin
 Application.OnHint:=ShowHint;

 Color:=ConfigInfo.BGColor;
 SetThreadData;
 TCtrl.Accessible:=false;
 TCtrl.Links0:=TStringList.Create;
 TCtrl.Links:=TStringList.Create;
 TCtrl.Thread:=TDisplayThread.Create(Self);

 Self.Caption:=AppName;
 DocHistory:=TStringList.Create;
 P:=ParamStr(1);
 HistoryIndex:=-1;
 Self.Document:=TDocument.Create;
 if ((P <> '') and  Self.OpenDocument(P)) then begin
  DocHistory.Add(Document.Location);
  Inc(HistoryIndex);
  HistoryToMenu;
  SetButtons;
 end;{else}
 {$IFDEF Delphi5}ToolBar1.Transparent:=true;{$ENDIF}
end;

procedure TMainForm.MenuOpenClick(Sender: TObject);
begin
  if OpenDialog1.Execute then
   if OpenDocument(OpenDialog1.FileName) then begin
    AddToHistory(OpenDialog1.FileName);
    HistoryIndex:=DocHistory.Count-1;
    SetButtons;
   end;
end;

(******************************************************************************
tryes to open new document
*****************************************************************************)
function TMainForm.OpenDocument(const FileName: ANSIString): boolean;
var D: TDocument;
begin
 Screen.Cursor:=crHourGlass;
 CurrLink:='';
 RESULT:=true;
 PauseThread;
 StatusBar1.SimpleText:='Loading file '+FileName;
 try
  D:=TDocument.OpenFile(FileName);
  Self.Document.Free;
  Self.Document:=D;
  Application.Title:=Document.Location + ' - '+ AppName;
  Self.Caption:=Application.Title;
 except
  on E: Exception do begin
    ShowMessage(E.Message);
    RESULT:=false;
  end;{on Exception}
 end;{try/e}
 ScrollBar1.Position:=0;
 SetThreadData;
 TCtrl.Content:=Document.FContent;
 TCtrl.ContentChanged:=true;
 UnpauseThread;
 LocationEdit.Text:=Document.Location;
 StatusBar1.SimpleText:='';
 Screen.Cursor:=crDefault;
end;

procedure TMainForm.MenuViewClick(Sender: TObject);
begin
 Document.ShowSource;
end;

procedure TMainForm.MenuExitClick(Sender: TObject);
begin
 Close;
end;

procedure TMainForm.MenuSettingsClick(Sender: TObject);
begin
 PauseThread;
 if ShowConfigForm then begin
  Color:=ConfigInfo.BGColor;
  SetDocumentFont;
  TCtrl.Thread.Priority:=ConfigInfo.Priority;
  TCtrl.ContentChanged:=true; 	// the font height may vary a bit...
 end;
 SetThreadData;		//... so we have to recalculate total height
 UnpauseThread;
end;

procedure TMainForm.LeftButtonClick(Sender: TObject);
begin
 if (HistoryIndex > 0) then begin
  Dec(HistoryIndex);
  OpenDocument(DocHistory[HistoryIndex]);
  SetButtons;
 end;{if}
 SetButtons;
end;

procedure TMainForm.RightButtonClick(Sender: TObject);
begin
 if (HistoryIndex < (DocHistory.Count-1)) then begin
  Inc(HistoryIndex);
  OpenDocument(DocHistory[HistoryIndex]);
  SetButtons;
 end;{if}
 SetButtons;
end;

procedure TMainForm.ReloadButtonClick(Sender: TObject);
var y: integer;
begin
 if (Self.Document.Location <> '') then begin
   y:=ScrollBar1.Position;
   if not OpenDocument(Self.Document.Location) then
     ShowMessage('Can''t reload document!')
   else begin
     if (y > 0) and (ScrollBar1.Position <= y) then
       ScrollBar1.Position:=y;
   end;
 end;
end;

procedure TMainForm.HistoryToMenu;
var I: integer;
    M: TMenuItem;
begin
 for I:=0 to (DocHistory.Count-1) do begin
  if ((MMenuGo.Count-GOINDEX) <= I) then begin
   M:=TMenuItem.Create(Self);             // create new menuitem
   MMenuGo.Add(M);                        // in Go menu
   M.OnClick:=MenuGoClick;
  end;{if}
  M:=MMenuGo.Items[I+GOINDEX];		// set caption & tag
  M.Caption:=DocHistory[I];
  M.Checked:=(HistoryIndex = I);
  M.Tag:=I;
 end;{for}
 for I:=(MMenuGo.Count-1) downto (DocHistory.Count+GOINDEX) do begin
  M:=MMenuGo.Items[I];                  // delete items we don't need
  MMenuGo.Delete(I);
  M.Free;
 end;{for}
end;

procedure TMainForm.MenuGoClick(Sender: TObject);
begin
  HistoryIndex:=(Sender as TMenuItem).Tag;
  OpenDocument(DocHistory[HistoryIndex]);
  SetButtons;
end;

procedure TMainForm.ScrollBar1Change(Sender: TObject);
begin
 TopY:=ScrollBar1.Position;
 SetThreadData;
end;

procedure TMainForm.FormPaint(Sender: TObject);
begin
 TCtrl.DoPaint:=true;
end;

procedure TMainForm.MenuHelpClick(Sender: TObject);
var HelpFile: ANSIString;
begin
 if Sender = MenuHelp then  HelpFile:='help.sml'
   else HelpFile:='readme.sml';
 HelpFile:=ExtractFilePath(Application.ExeName)+HelpFile;
 if OpenDocument(HelpFile) then begin
   AddToHistory(HelpFile);
   HistoryIndex:=DocHistory.Count-1;
   SetButtons;
 end;
end;

procedure TMainForm.AddToHistory(FileName: ANSIString);
var I: integer;
begin
 FileName:=ReplaceChar(FileName,'\','/');
 if (LocationEdit.Items.IndexOf(FileName) = -1) then
   LocationEdit.Items.Add(FileName);
 LocationEdit.SelectAll;

 if (DocHistory.Count > 5) then begin
  DocHistory.Delete(0);
  Dec(HistoryIndex);
 end;

 if (HistoryIndex < (DocHistory.Count-1)) then
   for I:=(DocHistory.Count-1) downto (HistoryIndex+1) do
     DocHistory.Delete(I);
 if (DocHistory.Count = 0) or (CompareText(DocHistory[DocHistory.Count-1],FileName) <> 0) then begin
   DocHistory.Add(FileName);
   Inc(HistoryIndex);
 end;{if}
 HistoryToMenu;
 SetButtons;
end;

procedure TMainForm.LocationEditKeyPress(Sender: TObject; var Key: Char);
begin
 if (Key = #13) then
  if OpenDocument(LocationEdit.Text) then begin
      AddToHistory(LocationEdit.Text);
      HistoryIndex:=DocHistory.Count-1;
      SetButtons;
  end;{if}
end;

function TMainForm.IsLink(x,y: integer;var S: shortstring): boolean;
var P: TPoint;
    I: integer;
begin
 RESULT:=false;
 P:=Point(X-TCtrl.Left,Y-TCtrl.Top);
 for I:=0 to (TCtrl.Links.Count-1) do
   if PtInRect(PRect(TCtrl.Links.Objects[I])^, P) then begin
    RESULT:=true;
    S:=ReplaceChar(TCtrl.Links[I],'\','/');
    BREAK;
   end;{if}
end;

procedure TMainForm.FormMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
begin
 if IsLink(x, y, CurrLink) then begin
  Cursor:=crHandPoint;
  StatusBar1.SimpleText:=CurrLink;
 end
 else begin
  Cursor:=crDefault;
  StatusBar1.SimpleText:='';
  CurrLink[0]:=#0;
 end;
end;

procedure TMainForm.FormClick(Sender: TObject);
var Link: ShortString;
begin
 Link:=CurrLink;
 if (Link <> '') then begin
  if OpenDocument(Link) then begin
    AddToHistory(Link);
    HistoryIndex:=DocHistory.Count-1;
    SetButtons;
  end;
 end;
end;

procedure TMainForm.FormClose(Sender: TObject;var Action: TCloseAction);
begin
 Screen.Cursor:=crHourGlass;
 TCtrl.Thread.Terminate;
end;

procedure TMainForm.ScrollBar1KeyDown(Sender: TObject; var Key: Word;Shift: TShiftState);
var NewPos: integer;
begin
 if (Key = vk_prior) then begin  // PageUp
  NewPos:=ScrollBar1.Position-TCtrl.Height+10;
  if (NewPos < 0) then NewPos:=0;
  ScrollBar1.Position:=NewPos;
 end
 else
 if (Key = vk_next) then begin    // PageDown
  NewPos:=ScrollBar1.Position+TCtrl.Height-10;
  if (NewPos > ScrollBar1.Max) then NewPos:=ScrollBar1.Max;
  ScrollBar1.Position:=NewPos;
 end
end;

end.

