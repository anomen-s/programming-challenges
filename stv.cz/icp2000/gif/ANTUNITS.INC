{******************************************************************************}
{**                                                                          **}
{**  Compiler options and derectives for AntUnits units set.                 **}
{**                                                                          **}
{**  Author:    KARPOLAN                                                     **}
{**  E-Mail:    karpolan@yahoo.com , karpolan@utilmind.com                   **}
{**  Home Page: http://karpolan.i.am, http://www.utilmind.com                **}
{**  Copyright © 1996-99 by KARPOLAN.                                        **}
{**                                                                          **}
{******************************************************************************}
{**  History:                                                                **}
{**                                                                          **}
{**  31 aug 1999 - Last modified... Prepared for public release.             **}
{******************************************************************************}

{*******************************************************************************
  This is determination of Delphi/CBuilder version.
*******************************************************************************}
{** Delphi 1 **}
{$IfDef VER80}
  {$Define Delphi}
  {$Define Delphi1}
  {$Define Delphi2andLower}
{$EndIf}

{** Delphi 2 **}
{$IfDef VER90}
  {$Define Delphi}
  {$Define Delphi2}
  {$Define Delphi2andLower}
{$EndIf}

{** CBuilder 1 **}
{$IfDef VER93}
  {$Define Builder}
  {$Define Builder1}
  {$Define Delphi2}
  {$Define Delphi2andLower}
{$EndIf}

{** Delphi 3 **}
{$IfDef VER100}
  {$Define Delphi}
  {$Define Delphi3}
{$EndIf}

{** CBuilder 3 **}
{$IfDef VER110}
  {$Define Builder}
  {$Define Builder3}
  {$Define Delphi3}
{$EndIf}

{** Delphi 4 **}
{$IfDef VER120}
  {$Define Delphi}
  {$Define Delphi4}
{$EndIf}

{** CBuilder 4 **}
{$IfDef VER125}
  {$Define Builder}
  {$Define Builder4}
  {$Define Delphi4}
{$EndIf}

{** Complex **}
{$IfNdef Delphi2andLower}
  {$Define Delphi3andHigher}

  {$IfNDef Delphi3}
    {$Define Delphi4andHigher}
  {$EndIf Delphi3}
{$EndIf}

{*******************************************************************************
  AntUnits_UseGif turn on/off using TGif as a registerd file format for TPicture
*******************************************************************************}
{$Define AntUnits_UseGif}

{*******************************************************************************
  AntUnits_UsePcx turn on/off using TPcx as a registerd file format for TPicture
*******************************************************************************}
{$Define AntUnits_UsePcx}

{*******************************************************************************
  DEDUG turn on/off some Debug messages and additional routines
*******************************************************************************}
// {$Define DEBUG}

