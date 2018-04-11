{$I hdr.inc}
unit About;

interface
uses
  Classes, Graphics, Controls, Forms, StdCtrls, Buttons, ExtCtrls;

type
  TAboutForm = class(TForm)
    Panel:      TPanel;
    BtnOk:      TBitBtn;
    Label1:     TLabel;
    Label2:     TLabel;
    Memo3:      TMemo;
    Bevel4:     TBevel;
    Label5:     TLabel;
    procedure   Label2Click(Sender: TObject);
  end;

implementation uses Windows, ShellAPI;
{$R *.DFM}

resourcestring
 URL = 'mailto:xxx@xxxx.xx';

procedure TAboutForm.Label2Click(Sender: TObject);
begin
 ShellExecute(Application.MainForm.Handle, nil, PChar(URL), nil, nil, SW_SHOWNOACTIVATE);
end;

end.


