unit splash;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs;

type
  TSplashForm = class(TForm)
    procedure   FormPaint(Sender: TObject);
  private
    FStatus:    shortstring;
  public
    { Public declarations }
  end;

procedure ShowProgress(Status: ShortString);
procedure DestroySplash;

var
  SplashForm: TSplashForm;

implementation
{$R *.DFM}

procedure ShowProgress(Status: ShortString);
var i: cardinal;
begin
 SplashForm.FStatus:=Status;
 SplashForm.Invalidate;
  i:=GetTickCount;
  repeat
   Application.ProcessMessages
  until GetTickCount > (i + 1*1000);
end;

procedure DestroySplash;
begin
 {$IFDEF DEBUG}BreakIf(SplashForm = nil, 'Multiple calling of DestroySplash');{$ENDIF}
 if SplashForm <> nil then SplashForm.Free;
 SplashForm:=nil;
end;

procedure TSplashForm.FormPaint(Sender: TObject);
begin
 self.Canvas.TextOut(1,1,FStatus);
 // show logo
end;

initialization
 SplashForm:=TSplashForm.CreateNew(Application);
 SplashForm.Visible:=true;
 SplashForm.Position:=poScreenCenter;
 SplashForm.BorderIcons:=[];
 SplashForm.BorderStyle:=bsNone;
 SplashForm.OnPaint:=SplashForm.FormPaint;
end.
