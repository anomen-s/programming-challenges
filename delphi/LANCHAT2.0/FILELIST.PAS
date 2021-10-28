{$I _hdr.inc}
unit FileList;
interface uses Classes, BigFiles;


type
 TFileList = class(TList)
 protected
  function 	Get(Index: Integer): TFile;
  procedure 	Put(Index: Integer; Item: TFile);
 public
  property 	Items[Index: Integer]: TFile read Get write Put; default;

  // returns index of TFile
  function 	IndexOf(const FileName: shortstring): integer;

  // adds non-NIL item (replaces over nil item or appends at end)
  function 	Add(Item: TFile): Integer;

  // deletes item and frees associated TFile object
  procedure	Delete(Index: integer);

  // returns index of file owned by specified group
{function 	gIndexOf(const FileName, Group: shortstring): integer;}
 end;

implementation uses Windows, SysUtils, MainUnit, ErrorF, Tools;

function TFileList.Get(Index: Integer): TFile;
begin
 {$IFDEF DEBUG}
  BreakIf((Index < 0) or (Index >= Count), 'Invalid index in TFile.Get!');
 {$ENDIF}
 RESULT:=inherited Get(Index);
end;

procedure TFileList.Put(Index: Integer; Item: TFile);
begin
 inherited Put(Index, Item);
end;

function TFileList.IndexOf(const FileName: shortstring): integer;
var I: integer;
begin
 RESULT:=-1;
 for I:=0 to (Count-1) do
   if ((Items[I] <> nil) and (Items[I].FileName = FileName))
     then begin RESULT:=I;EXIT;end;
end;

function TFileList.Add(Item: TFile): Integer;
var I: integer;
begin
 RESULT:=-1;
 if (Item = nil) then EXIT;
 for I:=0 to (Count-1) do
  if (Items[I] = nil) then begin
   RESULT:=I;
   Items[I]:=Item;
   EXIT;
  end;{if}
 RESULT:=inherited Add(Item);
end;

procedure TFileList.Delete(Index: integer);
begin
 {$IFDEF DEBUG}
  BreakIf((Index < 0) or (Index >= Count), 'Invalid index in TFile.Delete!');
 {$ENDIF}
  if (Items[Index] <> nil) then Items[Index].Free;
  inherited Delete(Index);
end;

end.

