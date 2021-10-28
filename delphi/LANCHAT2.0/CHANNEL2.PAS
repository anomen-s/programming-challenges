(******************************************************************)
(******************************************************************)

procedure TChannelForm.PaintBackground(var Message: TMessage);
var  x, y: Integer;
begin
  if not Dragging then begin
   y := 0;
   while (y < ClientHeight) do begin
     x := 0;
     while (x < ClientWidth) do begin
       Canvas.Draw(x, y, MainUnit.ChatwallPaper);
       x:=x+MainUnit.ChatWallPaper.Width;
     end;{while}
     y := y + MainUnit.ChatWallPaper.Height;
   end; {while}
  end;{if}
end;

procedure TChannelForm.FormResize(Sender: TObject);
begin
 ChatEdit.Top:=Self.ClientHeight-24;
 ChatEdit.Width:=clientWidth-8;
 ChatBox.Height:=Self.ClientHeight-28;
// SideList.Width:=ClientWidth-ChatBox.Width-ChatBox_SideList; { ta 4 je dulezita aby sidelist nepokryval cely form }
end;


