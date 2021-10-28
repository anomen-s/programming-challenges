{$I _hdr.inc}
unit Tools;
interface uses Windows, Forms;

//    problem cardinal/integer:
//	CRC je cardinal !
//	GetMailSlotInfo ma jeden parametr dword
//	ostatni integer
(*
type
 dwors = cardinal;
const
 max32bit = cardinal($FFFFffff);
*)


const
 CRLF   = #13+#10;

 PassLen = { length of password }
{$IFDEF DEBUG}	1 // heslo musi byt vzdy alespon 1 znak
{$ELSE}   	8
{$ENDIF}	;
const
 GroupsLimit  = 2;

 SHORT_PERIOD = 10;
 LONG_PERIOD  = 200;
 UserNamePrefix = 8 + 8 + 1;

type
 TAddress     = packed record // 127 bytes
                 case byte of
                 0: (S: string[126]);
                 1: (Len: byte;C: array[0..124] of char;Com: byte);
                 2: (A: array[0..126] of byte);
                end;
 TGroupName   = string[63];
 TUserName    = string[UserNamePrefix+30];
 TUserNick    = string[30];

const
 MaxPlugins   = 63;
// -------- Identifikacni pakety ------------------

// public message
// 0 = message
 amPublicMsg		= $80;

// chci jmena grup	    	vsem serverum
// ---
 amGroupNames		= $F1;

// jmeno usera
// ---
 amUser                 = $37;

// jmeno grupy			asi vsem
// 1=group name
 smGroupName 		= $3F;

// grupa zrusena
// 1=group name
 amGroupKO		= $30;

// uzivatel to vzdal (ukoncil LANCHmeAT }
// 1=nick
 amUserKO		= $31;

// ---------- Logovaci pakety -------------------

// nekdo se chce lognout   	prijemci (server)
//  0=group name
 cmLogIn 		= $03;
// odpoved na cmLogIn 		prijemci (Client)
//  0=group name / 1 = password
 smLogInReply		= $13;

//  ------- Soukrome packety: ------------
// Spolecna data:  0=group name / 1=password

// seznam uzivatelu		prijemci (Client)
// 2+=nicks
 smUserList 		= $12;
// chci seznam uzivatelu    	prijemci (Server)
 cmUserListReq 		= $02;
// seznam zprav			prijemci (client)
// 2=line index / 3+=lines
 smMsgList		= $15;
// chci starou zpravu
// 2=index / 3=pocet
 cmMsgReq		= $05;
// zprava od usera		prijemci (Server)
// 2=message
 cmMsg 			= $06;
// odhlaseni                    prijemci (Server)
 cmLogout		= $07;
// vykopnuti
 smKick			= $17;
// chci seznam souboru
 cmFileListReq		= $08;
// posilam seznam souboru
// 2+=filenames
 smFileList		= $18;
// posilam novej soubor
// 2=filename / 3=delka / 4=CRC  +data
 gmFile		        = $09;
// chci poslat soubor
// 2=filename
 gmFileReq              = $0A;

// END MSGFlags
const
STR_DestroyGrp	= 100;
STR_LogOut	= 101;
STR_NoInfo	= 102;
STR_AlreadyLogged=103;
STR_NickLenLimit= 104;
STR_DontWatch	= 105;
STR_AllFiles	= 106;
STR_TXTFiles	= 107;
STR_GroupExists	= 108;
STR_ForceClose	= 109;
STR_EnterGrpName= 110;
STR_AskClose	= 111;
STR_ChooseUser	= 112;
STR_AskStop	= 113;
STR_ClearChat	= 114;
STR_NickExists	= 115;
STR_SendPrivate = 116;
STR_NoSplit	= 117;


STR_VERSION	= 150;
STR_COPYRIGHT	= 151;

function RandomName(Len: byte): Shortstring;
Function CalcCRC(StartCRC: cardinal;var Buf;Size: integer): cardinal;
Function HexToInt(HexStr: Shortstring): integer;
function AddBSlash(const FileName: string): string;
function Name2Nick(UserName: TUserName): TUserNick;

{$IFDEF DEBUG}
procedure BreakIf(B: Boolean;const S: ANSIstring);
{$ENDIF}

implementation uses SysUtils;

{ *** HexToInt *** }
Function HexToInt(HexStr: Shortstring): integer;
var Hex: integer;
    I: byte;
begin
   Hex := 0;                                          { vysledek = 0 }
   HexStr:=UpperCase(HexStr);
   for I := 1 to Length(HexStr) do
   begin
    if (HexStr[I] in ['0'..'9','A'..'F']) then
    begin
     Hex := Hex shl 4;
     if (HexStr[I] >= 'A') then Inc(Hex, Ord(HexStr[I]) - 55)
     else Inc(Hex, Ord(HexStr[I]) - 48);
    end
    else begin
     {$IFDEF DEBUG}BreakIf(true,'HexToInt Error');{$ENDIF}
     RESULT:=0;
     EXIT;
    end;{else}
   end;
   RESULT:= Hex;
end;

function Name2Nick(UserName: TUserName): TUserNick;
var L: integer;
begin
 L:=Length(UserName)-UserNamePrefix;
 if (L > 0) then
  RESULT:=copy(UserName, UserNamePrefix+1, L)
 else
  RESULT:='';
end;

function  AddBSlash(const FileName: string): string;
var FName: string;
begin
 FName:=FileName;
 if FName[Length(FName)] <> '\' then FName:=FName+'\';
 Result:=UpperCase(FName);
end;

function RandomName(Len: byte): ShortString;
var I: integer;
begin
 RESULT:='';
 for I:=1 to Len do begin
  case (Random(50) > 30) of
   true:  RESULT:=RESULT+chr(Random(10)+ord('0'));
   false: RESULT:=RESULT+chr(Random(26)+ord('a'));
  end;{case}
 end;{for}
end;

var CRCTab: array[0..255] of cardinal;

{$RANGECHECKS OFF}

Procedure InitCRC;
var I, C, J: cardinal;
begin
 for I:=0 to 255 do begin
  C:=I;
  for J:=0 to 7 do if (C and 1)<>0 then C:=((C shr 1) xor cardinal($EDB88320)) else C:=C shr 1;
  CRCTab[I]:=C;
 end; // for I
end;

Function CalcCRC(StartCRC: cardinal;var Buf;Size: integer): cardinal;
type IArray = array[0..$3FFFFFF] of byte; { 64 MB should be enough}
var  I: integer;
begin
 {$IFDEF DEBUG}BreakIf((@Buf = nil) or (Size = 0),'CRCheck: no data');{$ENDIF}
 for I:=0 to (Size-1) do StartCRC := CRCTAB[Byte(StartCRC XOR cardinal(IArray(Buf)[I]))] XOR ((StartCRC SHR 8));
 RESULT:=StartCRC;
end;

{$IFDEF RangeChecking}
{$RANGECHECKS ON}
{$ENDIF}

{$IFDEF DEBUG}
procedure BreakIf(B: Boolean;const S: ANSIstring);
begin
 if B then
  if (windows.MessageBox(Application.Handle, PChar(S+#13'Pøerušit bìh?'), 'BreakIf', MB_YESNO or MB_ICONERROR or MB_APPLMODAL) <> IDNO) then
  asm
   int 3
  end;
end;
{$ENDIF}

initialization
 InitCRC;
end.

