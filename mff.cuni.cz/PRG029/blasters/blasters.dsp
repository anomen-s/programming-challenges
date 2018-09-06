# Microsoft Developer Studio Project File - Name="blasters" - Package Owner=<4>
# Microsoft Developer Studio Generated Build File, Format Version 6.00
# ** DO NOT EDIT **

# TARGTYPE "Win32 (x86) Application" 0x0101

CFG=blasters - Win32 Debug
!MESSAGE This is not a valid makefile. To build this project using NMAKE,
!MESSAGE use the Export Makefile command and run
!MESSAGE 
!MESSAGE NMAKE /f "blasters.mak".
!MESSAGE 
!MESSAGE You can specify a configuration when running NMAKE
!MESSAGE by defining the macro CFG on the command line. For example:
!MESSAGE 
!MESSAGE NMAKE /f "blasters.mak" CFG="blasters - Win32 Debug"
!MESSAGE 
!MESSAGE Possible choices for configuration are:
!MESSAGE 
!MESSAGE "blasters - Win32 Release" (based on "Win32 (x86) Application")
!MESSAGE "blasters - Win32 Debug" (based on "Win32 (x86) Application")
!MESSAGE 

# Begin Project
# PROP AllowPerConfigDependencies 0
# PROP Scc_ProjName ""
# PROP Scc_LocalPath ""
CPP=cl.exe
MTL=midl.exe
RSC=rc.exe

!IF  "$(CFG)" == "blasters - Win32 Release"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 0
# PROP BASE Output_Dir "Release"
# PROP BASE Intermediate_Dir "Release"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 0
# PROP Output_Dir "Release"
# PROP Intermediate_Dir "Release"
# PROP Ignore_Export_Lib 0
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_MBCS" /Yu"stdafx.h" /FD /c
# ADD CPP /nologo /W3 /GX /O2 /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_MBCS" /FD /c
# SUBTRACT CPP /YX /Yc /Yu
# ADD BASE MTL /nologo /D "NDEBUG" /mktyplib203 /win32
# ADD MTL /nologo /D "NDEBUG" /mktyplib203 /win32
# ADD BASE RSC /l 0x405 /d "NDEBUG"
# ADD RSC /l 0x405 /d "NDEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:windows /machine:I386
# ADD LINK32 winmm.lib ws2_32.lib OpenGL32.lib Glu32.lib lib/glpng.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:windows /machine:I386 /out:"blasters.exe"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# PROP BASE Use_MFC 0
# PROP BASE Use_Debug_Libraries 1
# PROP BASE Output_Dir "Debug"
# PROP BASE Intermediate_Dir "Debug"
# PROP BASE Target_Dir ""
# PROP Use_MFC 0
# PROP Use_Debug_Libraries 1
# PROP Output_Dir "Debug"
# PROP Intermediate_Dir "Debug"
# PROP Ignore_Export_Lib 0
# PROP Target_Dir ""
# ADD BASE CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_MBCS" /Yu"stdafx.h" /FD /GZ /c
# ADD CPP /nologo /W3 /Gm /GX /ZI /Od /D "WIN32" /D "_DEBUG" /D "_WINDOWS" /D "_MBCS" /FR /FD /GZ /c
# SUBTRACT CPP /YX /Yc /Yu
# ADD BASE MTL /nologo /D "_DEBUG" /mktyplib203 /win32
# ADD MTL /nologo /D "_DEBUG" /mktyplib203 /win32
# ADD BASE RSC /l 0x405 /d "_DEBUG"
# ADD RSC /l 0x405 /d "_DEBUG"
BSC32=bscmake.exe
# ADD BASE BSC32 /nologo
# ADD BSC32 /nologo
LINK32=link.exe
# ADD BASE LINK32 kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:windows /debug /machine:I386 /pdbtype:sept
# ADD LINK32 winmm.lib ws2_32.lib OpenGL32.lib Glu32.lib lib/glpngd.lib kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib /nologo /subsystem:windows /debug /machine:I386 /pdbtype:sept

!ENDIF 

# Begin Target

# Name "blasters - Win32 Release"
# Name "blasters - Win32 Debug"
# Begin Group "Source Files"

# PROP Default_Filter "cpp;c;cxx;rc;def;r;odl;idl;hpj;bat"
# Begin Source File

SOURCE=.\ai.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\blasters.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\client.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\game.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\gamedata.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\glgame.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\glinit.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\globals.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\gltext.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\gltools.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\inet.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\keyb.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\logger.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\menu.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\netdata.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\server.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI

!ENDIF 

# End Source File
# Begin Source File

SOURCE=.\StdAfx.cpp

!IF  "$(CFG)" == "blasters - Win32 Release"

# ADD CPP /Yc"stdafx.h"

!ELSEIF  "$(CFG)" == "blasters - Win32 Debug"

# ADD CPP /Zp4 /ZI
# SUBTRACT CPP /YX /Yc

!ENDIF 

# End Source File
# End Group
# Begin Group "Header Files"

# PROP Default_Filter "h;hpp;hxx;hm;inl"
# Begin Source File

SOURCE=.\ai.h
# End Source File
# Begin Source File

SOURCE=.\blasters.h
# End Source File
# Begin Source File

SOURCE=.\game.h
# End Source File
# Begin Source File

SOURCE=.\gamedata.h
# End Source File
# Begin Source File

SOURCE=.\glgame.h
# End Source File
# Begin Source File

SOURCE=.\glinit.h
# End Source File
# Begin Source File

SOURCE=.\globals.h
# End Source File
# Begin Source File

SOURCE=.\gltext.h
# End Source File
# Begin Source File

SOURCE=.\gltools.h
# End Source File
# Begin Source File

SOURCE=.\keyb.h
# End Source File
# Begin Source File

SOURCE=.\logger.h
# End Source File
# Begin Source File

SOURCE=.\menu.h
# End Source File
# Begin Source File

SOURCE=.\net.h
# End Source File
# Begin Source File

SOURCE=.\StdAfx.h
# End Source File
# End Group
# Begin Group "Resource Files"

# PROP Default_Filter "ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe"
# End Group
# Begin Source File

SOURCE=.\ReadMe.txt
# End Source File
# End Target
# End Project
