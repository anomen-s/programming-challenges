{$I _hdr.inc}

unit About;

interface

uses Windows, SysUtils, Classes, Graphics, Forms, Controls, StdCtrls,
  Buttons, ExtCtrls;

type
  TAboutBox = class(TForm)
    Panel1: 	TPanel;
    Author1: 	TImage;
    ProductName:TLabel;
    Version: 	TLabel;
    Copyright: 	TLabel;
    AboutTimer: TTimer;
    Author2: 	TImage;
    Bevel1: 	TBevel;
    Bevel2: 	TBevel;
    OKButton: 	TBitBtn;
    procedure 	FormActivate(Sender: TObject);
    procedure   SecretClick(Sender: TObject);
    procedure   PrintJoke(Sender: TObject);
    procedure   AboutTimerTimer(Sender: TObject);
    procedure   OKButtonKeyPress(Sender: TObject; var Key: Char);
   public
    WatchCount: integer; { :-) }
    Secret:	integer;
    TimerI:	byte;
  end;

var AboutBox: TAboutBox;

implementation uses Dialogs, Tools;
{$R *.DFM}

const XErrorCount = 46;
      XMsgsCount = 5;
      XDictCount = 2;

procedure TAboutBox.FormActivate(Sender: TObject);
begin
 Randomize;
 AboutTimer.Enabled:=false;
 Author2.OnClick:=PrintJoke;
 OKButton.OnKeyPress:=OKButtonKeyPress;
 Copyright.Font.Color:=clWindowText;
 Copyright.Caption:=LoadStr(STR_COPYRIGHT);
 Version.Caption:=LoadSTR(STR_VERSION);
 Secret:=0;
 Inc(AboutBox.WatchCount);
 if (AboutBox.WatchCount > 5) and (Random(50) < 20) then
   ShowMessage(LoadStr(STR_DontWatch));
end;

procedure TAboutBox.SecretClick(Sender: TObject);
var I: integer;
begin
 if (Sender = Author1) then I:=0
 else
  if (Sender = Version) then I:=1
  else
   if (Sender = Copyright) then I:=2
   else
    if (Sender = ProductName) then I:=3
    else I:=-1;
 if (Secret = I) then Inc(Secret) else Secret:=0;
 if (Secret = 4) then begin
  Secret:=0;
  ShowMessage(LoadStr(250+Random(XMsgsCount+1)));
 end;{if}
end;

procedure TAboutBox.PrintJoke(Sender: TObject);
begin
 Copyright.Caption:=LoadStr(200+Random(XErrorCount+1));
 Self.AboutTimer.Enabled:=true;
{$IFNDEF DEBUG}
 Author2.OnClick:=nil;
{$ENDIF}
end;

procedure TAboutBox.AboutTimerTimer(Sender: TObject);
var Color: integer;
begin
 if (TimerI = 0) then Color:=clRed else Color:={clNavy}clBlack;
 Copyright.Font.Color:=color;
 TimerI:=TimerI xor $FF;
end;

procedure TAboutBox.OKButtonKeyPress(Sender: TObject; var Key: Char);
begin
 if Key = '?' then begin
 ShowMessage(LoadStr(300+Random(XDictCount+1)));
{$IFNDEF DEBUG}
 OKButton.OnKeyPress:=nil;
{$ENDIF}
 end;
end;

end.


