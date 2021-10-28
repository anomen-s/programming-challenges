unit DLLMgr;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls,
  Forms, Dialogs;

type
  TPluginForm = class(TForm)
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  PluginForm: TPluginForm;

implementation uses Tools, PackUnit;
{$R *.DFM}

type
 PDLLInterface = ^TDLLInterface;
 TDLLInterface = record
   Init:        function: boolean;
   Send:        procedure(const Dest: TAddress;XPacket: TPacket);
   Broadcast:   procedure(XPacket: TPacket);
   IsNew:       function: boolean;
   Receive:     function(XPacket: TPacket): boolean;
   Done:        procedure;
 end;
var
 DLLInterfaces: array[0..MaxPlugins] of PDLLInterface;

end.
