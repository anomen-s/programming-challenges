{$I hdr.inc}
{$DESCRIPTION 'ICP''2000 Correspondence stage solution'}
{$EXTENSION exe}
program ICP2000;

uses
  Forms,
  JPEG,   // JPEG images support (standard Delphi unit)
  AntGif in '..\GIF\antgif.pas',// GIF images support (C) 1999, UtilMind Solutions
  MainUnit in 'MainUnit.pas' {MainForm},
  Display in 'Display.pas',
  About in 'About.pas' {AboutForm},
  styles in 'styles.pas',
  FStream in 'FStream.pas',
  DocUnit in 'DocUnit.pas' {SourceForm},
  Config in 'config.pas' {ConfigForm}
  ;

{$R *.RES}
{$R DocUnit.RES}
begin
  Application.Initialize;
  Application.Title := 'SML Viewer';
  Application.CreateForm(TMainForm, MainForm);
  Application.Run;
end.

