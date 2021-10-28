{$I _hdr.inc}
unit InfoF;

interface

uses Windows, SysUtils, Classes, Graphics, Forms, Controls, StdCtrls,
  Buttons, ExtCtrls,
  Tools;

type
  TInfoForm = class(TForm)
    Bevel1:     TBevel;
    NickLabel:  TLabel;
    OKBtn:	TBitBtn;
    CancelBtn:	TBitBtn;
    CompEdit:   TEdit;
    NickEdit: 	TEdit;
    CompLabel: TLabel;
    procedure 	FormPaint(Sender: TObject);
    procedure 	FormCreate(Sender: TObject);
    function	Execute: boolean;
    procedure 	IsNickValid(Sender: TObject);
    procedure 	FormActivate(Sender: TObject);
  private
    WallPaper: 	TBitmap;
  public
    OldNick: 	TUserName;
    ReadOnly:	boolean;
  end;

var InfoForm: 	TInfoForm;

implementation uses dialogs, MainUnit, PublicF, userList;
{I constant.pas}
{$R *.DFM}

procedure TInfoForm.FormPaint(Sender: TObject);
var  x, y: Integer;
begin
  y := 0;
  while y < ClientHeight do begin
    x := 0;
    while x < ClientWidth do begin Canvas.Draw(x, y, WallPaper);x:=x+WallPaper.Width;end;
    y := y + WallPaper.Height;
  end; {while}
end;

procedure TInfoForm.FormCreate(Sender: TObject);
//var ResStream: TResourceStream;
begin
 WallPaper:=TBitMap.Create;
 WallPaper.LoadFromResourceID(Hinstance, 3);
(*ResStream:=TResourceStream.CreateFromID(HInstance, 1, RT_RCDATA);
  try
   WallPaper:=TBitmap.Create;
   WallPaper.LoadFromStream(ResStream);
  finally
   ResStream.Free;
  end;{try}*)
end;

function TInfoForm.Execute: boolean;
var I: integer;
begin
 OldNick:=LANCHUsers.LocalUser;
 NickEdit.Text:=OldNick;
 NickEdit.SelectAll;
 NickEdit.ReadOnly:=Self.ReadOnly;
 I:=ShowModal;
 RESULT:=false;
 if (I = mrOk)
  and (not Self.ReadOnly)          // lze menit jmeno ?
   and (NickEdit.Text <> '')	   // bylo zadano jmeno ?
   and (NickEdit.Text <> OldNick) then // bylo zadano NOVE jmeno ?
{  and (NickEdit.Text <> 'ptn') >>>  }
  if LANCHUsers.UserStatus(NickEdit.Text) = uOk then    // zadane jmeno uz existuje ?
   ShowMessage(LoadStr(STR_NickExists))
   else begin
//  if (UpperCase(NickEdit.Text) = 'STOUPA') then
//   begin raise Exception.Create('Warning: Intelligence not found !');{asm cli;hlt;end;}end;
    LANCHUsers.SetLocalUser(NickEdit.Text);
    RESULT:=true;
   end;{if}
end;

procedure TInfoForm.IsNickValid(Sender: TObject);
begin
 Self.OKBtn.Enabled:=(Self.NickEdit.Text <> '');
 if Length(Self.NickEdit.Text) = 30 then ShowMessage(LoadStr(STR_NickLenLimit));
end;

procedure TInfoForm.FormActivate(Sender: TObject);
begin
  NickEdit.SetFocus;
  IsNickValid(Sender);
end;


end.

