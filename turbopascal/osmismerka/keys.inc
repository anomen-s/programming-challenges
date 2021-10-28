(* VersionNum: 1.25
{  **************************************************************  }
{  *                    Keyboard Scan Codes                     *  }
{  *                                                            *  }
{  * typ: sub-INClude                                           *  }
{  *                                                            *  }
{  **************************************************************  }

*)

const
 Null      =   #0; { znak NULL }
 BS        =   #8; { klavesa BACKSPACE }
 Tab       =   #9;
 CR        =  #13; { klavesa ENTER }
 Esc       =  #27; { klavesa ESC }
 Space     =  #32; { mezernik }
 ShiftTab  = #143; { Shift + Tab }

 Alt1      = #248; { Alt + 1 }
 Alt2      = #249; { Alt + 2 }
 Alt3      = #250; { Alt + 3 }
 Alt4      = #251; { Alt + 4 }
 Alt5      = #252; { Alt + 5 }
 Alt6      = #253; { Alt + 6 }
 Alt7      = #254; { Alt + 7 }
 Alt8      = #255; { Alt + 8 }
 Alt9      = #256; { Alt + 9 }
 Alt0      = #257; { Alt + 0 }
 AltMinus  = #258; { Alt + '-' }
{   Alt       = #259; { Alt + '=' }

 AltQ      = #144; { Alt + Q }
 AltW      = #145; { Alt + W }
 AltE      = #146; { Alt + E }
 AltR      = #147; { Alt + R }
 AltT      = #148; { Alt + T }
 AltY      = #149; { Alt + Y }
 AltU      = #150; { Alt + U }
 AltI      = #151; { Alt + I }
 AltO      = #152; { Alt + O }
 AltP      = #153; { Alt + P }

 AltA      = #158; { Alt + A }
 AltS      = #159; { Alt + S }
 AltD      = #160; { Alt + D }
 AltF      = #161; { Alt + F }
 AltG      = #162; { Alt + G }
 AltH      = #163; { Alt + H }
 AltJ      = #164; { Alt + J }
 AltK      = #165; { Alt + K }
 AltL      = #165; { Alt + L }
 AltZ      = #172; { Alt + Z }
 AltX      = #173; { Alt + X }
 AltC      = #174; { Alt + C }
 AltV      = #175; { Alt + V }
 AltB      = #176; { Alt + B }
 AltN      = #177; { Alt + N }
 AltM      = #178; { Alt + M }

 F1        = #187; { funkcni klic 1 }
 F2        = #188; { funkcni klic 2 }
 F3        = #189; { funkcni klic 3 }
 F4        = #190; { funkcni klic 4 }
 F5        = #191; { funkcni klic 5 }
 F6        = #192; { funkcni klic 6 }
 F7        = #193; { funkcni klic 7 }
 F8        = #194; { funkcni klic 8 }
 F9        = #195; { funkcni klic 9 }
 F10       = #196; { funkcni klic 10 }
{ F11       = #261; { funkcni klic 11 }
{ F12       = #262; { funkcni klic 12 }
 F11       = #133; { funkcni klic 11 }
 F12       = #134; { funkcni klic 12 }
 ShiftF1   = #212; { Shift + F1 }
 ShiftF2   = #213; { Shift + F2 }
 ShiftF3   = #214; { Shift + F3 }
 ShiftF4   = #215; { Shift + F4 }
 ShiftF5   = #216; { Shift + F5 }
 ShiftF6   = #217; { Shift + F6 }
 ShiftF7   = #218; { Shift + F7 }
 ShiftF8   = #219; { Shift + F8 }
 ShiftF9   = #220; { Shift + F9 }
 ShiftF10  = #221; { Shift + F10 }
 ShiftF11  = #263; { Shift + F11 }
 ShiftF12  = #264; { Shift + F12 }
 CtrlF1    = #222; { Ctrl + F1 }
 CtrlF2    = #223; { Ctrl + F2 }
 CtrlF3    = #224; { Ctrl + F3 }
 CtrlF4    = #225; { Ctrl + F4 }
 CtrlF5    = #226; { Ctrl + F5 }
 CtrlF6    = #227; { Ctrl + F6 }
 CtrlF7    = #228; { Ctrl + F7 }
 CtrlF8    = #229; { Ctrl + F8 }
 CtrlF9    = #230; { Ctrl + F9 }
 CtrlF10   = #231; { Ctrl + F10 }
 CtrlF11   = #265; { Ctrl + F11 }
 CtrlF12   = #266; { Ctrl + F12 }
 AltF1     = #232; { Alt + F1 }
 AltF2     = #233; { Alt + F2 }
 AltF3     = #234; { Alt + F3 }
 AltF4     = #235; { Alt + F4 }
 AltF5     = #236; { Alt + F5 }
 AltF6     = #237; { Alt + F6 }
 AltF7     = #238; { Alt + F7 }
 AltF8     = #239; { Alt + F8 }
 AltF9     = #240; { Alt + F9 }
 AltF10    = #241; { Alt + F10 }
 AltF11    = #267; { Alt + F11 }
 AltF12    = #268; { Alt + F12 }

 Home      = #199; { klavesa HOME }
 Up        = #200; { klavesa sipka nahoru }
 PgUp      = #201; { klavesa PgUp }
 Left      = #203; { klavesa sipka vlevo }
 Right     = #205; { klavesa sipka vpravo }
 EndK      = #207; { klavesa END }
 Down      = #208; { klavesa sipka dolu }
 PgDn      = #209; { klavesa PgDn }
 Ins       = #210; { klavesa INS }
 Del       = #211; { klavesa DEL }
 CtrlLeft  = #243; { Ctrl + sipka vlevo }
 CtrlRight = #244; { Ctrl + sipka vpravo }
 CtrlEnd   = #245; { Ctrl + klavesa End }
 CtrlPgDn  = #246; { Ctrl + klavesa PgDn }
 CtrlHome  = #247; { Ctrl + klavesa Home }
 CtrlPgUp  = #260; { Ctrl + klavesa PgUp }
 CtrlPrnScr= #242; { Ctrl + Print Screen }

const
 ScrLock   =  $10;             { deklarace p©¡znak– kl ves }
 NumLock   =  $20;
 CapsLock  =  $40;
 InsKey    =  $80;

const
 On  = True;
 Off = False;

