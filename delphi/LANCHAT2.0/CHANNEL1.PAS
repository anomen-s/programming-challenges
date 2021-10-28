(*                             { smFile }
procedure TChannelForm.cSaveFile(var XPacket: TPacket);
var Stream: TFileStream;
begin
 {$IFDEF DEBUG}if IsServer then ShowMessage('Server pouziva cSaveFile !');{$ENDIF}
// if (not IsServer) then begin  { client }
  if  StrToInt(XPacket.Lines[4]) <> XPacket.DataSize then Error('Nesouhlasi delka souboru !');
  MainForm.SaveDlg.FileName:=XPacket.Lines[3];
  MainForm.SaveDlg.Filter:=LoadStr(STR_AllFiles);
  if MainForm.SaveDlg.Execute then begin
   {$IFDEF DEBUG} if (XPacket.IDCode <> smFile) then ShowMessage('Chyba v SaveFile');{$ENDIF}
   Stream:=TFileStream.Create(MainForm.SaveDlg.FileName, fmCreate or fmShareDenyWrite);
   Stream.Write(XPacket.Data^, XPacket.DataSize);
   Stream.Free;
  end{if}
//end;{if}
end;*)

// when user double clicks on SideList
procedure TChannelForm.sSaveFile(Name: Shortstring);
var I: integer;
begin
 {$IFDEF DEBUG}
  BreakIf(not IsServer, 'Client pouziva sSaveFile !');
 {$ENDIF}
 I:=Files.IndexOf(Name);
 if not (((Files[I].Status and  stComplete) = 0) and (MessageDlg('Soubor není kompletní.'+#13+#10+'Chcete ho opravdu uložit na disk?', mtWarning, [mbYes, mbNo], 0)<> mrYes)) then
  if (I <> -1) then
    Files[I].Save
   else CriticalError('soubor neexistuje');
end;
                         { gmFile }
// received file packet
function TChannelForm.AddFile(var XPacket: TPacket): boolean;
var I: integer;
    F: TFile;
begin
 RESULT:=false;
 F:=TFile.ReceiveFile(XPacket);
 I:=Files.IndexOf(XPacket[3]);
 if (I <> -1) then Files.Delete(I);  // file already exists
 Files.Add(F);
end;

procedure TChannelForm.sRemoveFile(FileName: Shortstring);
var I: integer;
begin
 I:=Files.IndexOf(FileName);
 if (I = -1) then CriticalError('RemoveFile: Soubor neexistuje!')
   else Files.Delete(I);
end;

// sending file - event on MenuItem "Send file"
procedure TChannelForm.SendFile(Sender: TObject);
var F: TFile;
    I: integer;
begin
 if MainForm.OpenDlg.Execute then begin
//FileName:=MainForm.OpenDlg.FileName;
  try
    F:=TFile.LoadFile(MainForm.OpenDlg.FileName);
  except
    CriticalError(GrpName+': nepovedlo se naèíst soubor');
    EXIT;
  end;{try/e}

  if IsServer then begin		// server
   I:=Files.IndexOf(F.FileName);
   if (I <> -1) then
    if (MessageDlg('Soubor ji existuje, pøepsat ?', mtWarning, [mbYes, mbNo], 0) = mrYes) then
      begin
        Files.Delete(I);
        Files.Add(F);
      end{if}
    else F.Free
   else begin Files.Add(F);sCreateFilelistPacket;SendToUsers;end;
  end{if}
  else begin                         // client
   F.Send(SelfGP, ServerNick, gmFile);
  end;{else}

 end;{if - OpenDlg}
end;{PROC SendFile}


