{$IFDEF LocalDEBUG}	{$DEFINE DEBUGINFO}	{$ENDIF}
{$IFDEF BUG}		{$DEFINE DEBUGINFO}	{$ENDIF}
{$IFDEF DEBUGGER}	not supported   	{$ENDIF}
{$IFDEF DEBUG}          {$DEFINE DEBUGINFO}     {$ENDIF}

{$IFDEF DEBUGINFO}
	{$RANGECHECKS ON}       {$DEFINE RangeChecking}
	{$OVERFLOWCHECKS ON}
        {$VARSTRINGCHECKS ON}

        {$ASSERTIONS ON}

	{OPTIMIZATION OFF}

        {$WARNINGS ON}
        {$HINTS ON}
{$ELSE}
       	{$RANGECHECKS OFF}
        {$OVERFLOWCHECKS OFF}
        {$VARSTRINGCHECKS OFF}


        {$ASSERTIONS OFF}

	{$OPTIMIZATION ON}

        {$WARNINGS OFF}
        {$HINTS OFF}
{$ENDIF}

	{$DEBUGINFO ON}         // does not affect the size
        {$REFERENCEINFO ON}     // or speed of the executable
        {$LOCALSYMBOLS ON}      // program

{$LongStrings OFF}
{$BoolEval OFF}
{$WRITEABLECONST OFF}

{$IOCHECKS ON}
{$EXTENDEDSYNTAX ON}
{$MINENUMSIZE 4}
{$TYPEDADDRESS OFF}
{$ALIGN ON}

{$IFDEF VER130} {$Define Delphi5}       {$ENDIF VER130}
{$IFDEF VER120} {$Define Delphi4}       {$ENDIF VER120}
{$IFDEF VER100} {$Define Delphi3}       {$ENDIF VER100}


