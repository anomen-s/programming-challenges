
{ ********************************************************* }
{ *                                                       * }
{ *            LANCHmeAT 2.0  (c) PTN & D.M.              * }
{ *                                                       * }
{ *                                                       * }
{ ********************************************************* }

{$DESCRIPTION 'LANCHmeAT by PTN and D.M.'}

{$I _hdr.inc}
program LANCHAT;

uses
  splash in 'splash.pas' {SplashForm},
  Forms,
  dialogs,
  Windows,
  MainUnit in 'MainUnit.pas' {MainForm},
  About in 'About.pas' {AboutBox},
  FileList in 'FileList.pas',
  ChannelF in 'ChannelF.pas' {ChannelForm},
  InfoF in 'InfoF.pas' {InfoForm},
  GroupsF in 'Groupsf.pas' {GroupForm},
  ErrorF in 'ErrorF.pas' {ErrorForm},
  PackUnit in 'PackUnit.pas',
  PublicF in 'PublicF.pas' {PublicForm},
  DirDlg in 'DirDlg.pas',
  userlist in 'userlist.pas',
  BigFiles in 'BigFiles.pas',
  Tools in 'Tools.pas',
  DLLMgr in 'DLLMgr.pas' {PluginForm};

{$R *.RES}
{$R chat1.res}

var hMutex: THandle;
{$IFNDEF LocalDEBUG}
    Wnd: HWnd;
{$ENDIF}

begin
 hMutex:= CreateMutex(nil, False, 'LANCHmeAT');
{$IFNDEF LocalDEBUG}
 if (WaitForSingleObject(hMutex, 0) = Wait_TimeOut) then begin
   ShowMessage('Už máte LANCHmeAT spuštìný');
   Wnd := FindWindow('TMainForm', 'LANCHmeAT');
   SetForegroundWindow(Wnd);    // do hajzlu, proc to nefacha >>>
 end{if}
 else begin
{$ENDIF}
  Application.Initialize;
  Application.Title := 'LANCHmeAT 2.0';
  Application.CreateForm(TMainForm, MainForm);
  ShowProgress('Creating About box');
  Application.CreateForm(TAboutBox, AboutBox);
  ShowProgress('Creating Info Form');
  Application.CreateForm(TInfoForm, InfoForm);
  ShowProgress('Creating Public Channel');
  Application.CreateForm(TPublicForm, PublicForm);
  ShowProgress('Creating Group Form');
  Application.CreateForm(TGroupForm, GroupForm);
  DestroySplash;
  Application.Run;
  end;{else}
 ReleaseMutex(hMutex);
end.


