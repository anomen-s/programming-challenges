{$I hdr.inc}
unit config;

interface

uses Windows, Classes, Controls, Forms, StdCtrls, Buttons, ExtCtrls, Dialogs;

type
  TConfigForm = class(TForm)
    DirEdit: 	TEdit;
    Label1: 	TLabel;
    SaveBtn: 	TBitBtn;
    CancelBtn: 	TBitBtn;
    ColorDlg: 	TColorDialog;
    FontBox: 	TComboBox;
    Label2: 	TLabel;
    ColorPanel: TPanel;
    PriorityBox:TRadioGroup;
    PanelItalic:TPanel;
    PanelBold: 	TPanel;
    procedure 	SaveBtnClick(Sender: TObject);
    procedure 	FormCreate(Sender: TObject);
    procedure 	BgColorBtnClick(Sender: TObject);
    procedure 	PanelStyleClick(Sender: TObject);
    procedure   FontBoxChange(Sender: TObject);
  end;

var
 ConfigInfo: record           // this record holds all
    StylePath:	ANSIString;   // settings user can change
    FontName:	string[LF_FACESIZE];
    BGColor:	integer;
    Priority:	TThreadPriority;
    Bold:	boolean;
    Italic:	boolean;

    DefaultFontHeight: integer;
 end;

function ShowConfigForm: boolean;

implementation uses Registry, Graphics, SysUtils;
{$R *.DFM}

resourcestring
    RegKey = 'Software\PTN\SMLviewer';
    valSTYDir = 'STYDir';
    valFont = 'Font';
    valcolor = 'BGColor';
    valPriority = 'Priority';
    valBold = 'FontBold';
    valItalic = 'FontItalic';

function ShowConfigForm: boolean;
var F: TConfigForm;
begin
 try
  Screen.Cursor:=crHourGlass;
  F:=TConfigForm.Create(Application.MainForm);
 finally
  Screen.Cursor:=crDefault;
 end;{try/f}
 try
  RESULT:=(F.ShowModal = F.SaveBtn.ModalResult);
 finally
  F.Free;
 end;{try/f}
end;

(********************************************************************
saves settings from registry (when you press Save button)
*********************************************************************)
Procedure SaveConfig;
var R: TRegistry;
begin
 R:=TRegistry.Create;
 try
  R.RootKey:=HKEY_CURRENT_USER;
  R.OpenKey(RegKey,true);
  R.WriteString(valSTYDir, ConfigInfo.StylePath);
  R.WriteString(valFont, ConfigInfo.FontName);
  R.WriteInteger(valColor, ConfigInfo.BGColor);
  R.WriteInteger(valPriority, integer(ConfigInfo.Priority));
  R.WriteBool(valBold,ConfigInfo.Bold);
  R.WriteBool(valItalic,ConfigInfo.Italic);
 finally
  R.Free;
 end;{try/e}
end;

(********************************************************************
loads settings from registry (only on program startup)
*********************************************************************)
Procedure LoadConfig;
var R: TRegistry;
begin
 R:=TRegistry.Create;
 try
  R.RootKey:=HKEY_CURRENT_USER;
  R.OpenKey(RegKey, true);
  if R.ValueExists(valSTYDir) then ConfigInfo.StylePath:=R.ReadString(valSTYDir);
  if R.ValueExists(valFont) then ConfigInfo.FontName:=R.ReadString(valFont);
  if R.ValueExists(valColor) then ConfigInfo.BGColor:=R.ReadInteger(valColor);
  if R.ValueExists(valPriority) then ConfigInfo.Priority:=TThreadPriority(R.ReadInteger(valPriority));
  if R.ValueExists(valBold) then ConfigInfo.Bold:=R.ReadBool(valBold);
  if R.ValueExists(valItalic) then ConfigInfo.Italic:=R.ReadBool(valItalic);
 finally
  R.Free;
 end;{try/e}
end;

procedure TConfigForm.SaveBtnClick(Sender: TObject);
begin
 ConfigInfo.StylePath:=DirEdit.Text;
 ConfigInfo.BGColor:=ColorPanel.Color;
 ConfigInfo.FontName:=FontBox.Text;
 ConfigInfo.Priority:=TThreadPriority(PriorityBox.ItemIndex*2);
 ConfigInfo.Bold:= (PanelBold.BevelOuter = bvLowered);
 ConfigInfo.Italic:= (PanelItalic.BevelOuter = bvLowered);
 SaveConfig;
end;

const
 Bevels: array[Boolean] of TPanelBevel = (bvRaised, bvLowered);

procedure TConfigForm.FormCreate(Sender: TObject);
begin
 DirEdit.Text:=ConfigInfo.StylePath;
 FontBox.Items.Assign(Screen.Fonts);
 FontBox.Text:=ConfigInfo.FontName;
 ColorPanel.Color:=ConfigInfo.BGColor;
 PriorityBox.ItemIndex:=integer(ConfigInfo.Priority) div 2;
 PanelBold.BevelOuter:=Bevels[ConfigInfo.Bold];
 PanelItalic.BevelOuter:=Bevels[ConfigInfo.Italic];
end;

procedure TConfigForm.BgColorBtnClick(Sender: TObject);
begin
 ColorDlg.Color:=ColorPanel.Color;
       // we have to add current color to custom colors
       // for case it isn't in default set
 ColorDlg.CustomColors.Values['ColorI']:=IntToHex(ColorPanel.Color,6);
 if ColorDlg.Execute then
   ColorPanel.Color:=ColorDlg.Color and $FFffff;
end;

procedure TConfigForm.PanelStyleClick(Sender: TObject);
var B: ^TPanelBevel;
    FS: TFontStyles;
begin
 B:=@TPanel(Sender).BevelOuter;
 if (B^ = bvRaised) then B^:=bvLowered
   else B^:=bvRaised;

 FS:=[];
 if (PanelBold.BevelOuter = bvLowered) then Include(FS, fsBold);
 if (PanelItalic.BevelOuter = bvLowered) then Include(FS, fsItalic);
 ColorPanel.Font.Style:=FS;
 TPanel(Sender).Invalidate;
end;

procedure TConfigForm.FontBoxChange(Sender: TObject);
begin
 ColorPanel.Font.Name:=FontBox.Text;
end;

initialization
 ConfigInfo.StylePath:=ExtractFilePath(Application.ExeName);
 ConfigInfo.FontName:='Times New Roman';
 ConfigInfo.BGColor:=$808080;
 ConfigInfo.Priority:=tpIdle;
 ConfigInfo.Bold:=false;
 ConfigInfo.Italic:=false;

 ConfigInfo.DefaultFontHeight:=12;

 LoadConfig;
end.

