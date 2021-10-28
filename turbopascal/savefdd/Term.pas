(* VersionNum: 1.10
{  **************************************************************  }
{  *                   Termination Procedure                    *  }
{  *                                                            *  }
{  * typ: INClude                                               *  }
{  *                                                            *  }
{  **************************************************************  }

Procedure Term(Code: byte;S: string);
Procedure Terminate(_Code: word);

*)

Procedure Term(_Code: byte;_S: string);
begin
 WriteLn(_S);
 Halt(_Code);
end;

const
 ErrorListSize = 7;
 ErrorList : array[0..ErrorListSize] of string [21] =(
{ '| <-- MaxLength --> |' }
 ('Program finished'),
 ('Terminated by user'),
 (''),
 ('Missing Parameter'),
 ('Disk Read Error'),
 ('Disk Write Error'),
 (''),
 (''));

Procedure Terminate(_Code: word);
begin
 asm
  mov	ah, 02
  xor	bx, bx
  mov	dx, 1800h
  int	10h
 end;
 if _Code <= ErrorListSize then WriteLn(ErrorList[_Code])
   else WriteLn('Unknown Error');
 Halt(_Code);
end;
