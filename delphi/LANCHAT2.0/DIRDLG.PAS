{$I _hdr.inc}

{ *** This code was written by unknown author *** }

unit DirDlg;

interface uses Windows;

function BrowseDirectoryMP(const Title: PChar): ShortString;

implementation uses Forms, ShlObj, ActiveX;

// And here is the callback function:

function BrowseCallbackProc(Wnd: HWnd; Msg: UINT; lParam: LPARAM;lData: LPARAM): integer; stdcall;
begin
 Result := 0;
 {upon startup, set the selection to the intial directory desired}
 if (Msg = BFFM_INITIALIZED) then begin
   SendMessage(Wnd, BFFM_SETSELECTION, WPARAM(False), lData);
 end; {if}
end;

var InitDir: ShortString =  'c:\';


function BrowseDirectoryMP({AppHandle: HWnd;}const {InitDir,} Title: PChar): ShortString;
{Handle is the parent of the BrowseDirectory dialog window, while
 InitialDir is the directory which is selected when the dialog window
 is opened.}
var
  MyShellMalloc: IMalloc;     // IMalloc task allocator
  MyBrowseInfo: TBrowseInfo;
  DestDir: shortString;
  shBuff: PChar;
  MyItemIDList, TheItemIDList, SelectionIDList: PItemIDList;
  ShellFolder: IShellFolder;        	 // the powerful IShellFolder interface
  OLEStr: array[0..MAX_PATH] of TOLEChar;// need to use OLE strings
  Eaten, Attr: ULONG;
  Success: Boolean;
begin
  {This call is necessary as it retrieves a pointer to the IMalloc interface
  of the Win95 shell, which in turn is used to free memory that was allocated
  by the shell; something that certain shell functions require.}

  SHGetMalloc(MyShellMalloc);

  {Initialise destination string to be empty and set its length to MAX_PATH}

  DestDir := '';
//  SetLength(DestDir, MAX_PATH);

  {The pszDisplayName member of the TSHBrowseInfo structure needs to be
  allocated space via the shell's IMalloc interface}

  shBuff := PChar(MyShellMalloc.Alloc({MAX_PATH}255));

  {if allocation is sucessful then proceed}

  if assigned(shBuff) then begin
    try
     {Retrieve a pointer to an item identifier list specifying the location
     of the My Computer virtual folder relative to the desktop folder}

     SHGetSpecialFolderLocation(Application.Handle, CSIDL_DRIVES, MyItemIDList);
     try
      {MyItemIDList will be the root folder for the Browse Directory
      dialog. But what if you want a directory to be initially selected?
      Well, you first need to retrieve its item identifier. We do this
      via the IShellFolder interface for the desktop folder}

      if SHGetDesktopFolder(ShellFolder) = NO_ERROR then begin

        {The ParseDisplayName method will do the trick. But we need to
        make sure our directory string is a null-terminated Unicode string
        We use the StringToWideChar function to convert it properly}

        if ShellFolder.ParseDisplayName(Application.Handle, nil,
             StringToWideChar(InitDir, OLEStr, MAX_PATH), Eaten,
             SelectionIDList, Attr) = NO_ERROR then
              Success := True
            else
              Success := False;
      end{if}
      else
       Success := False;

       {Before calling the function which brings up the dialog editor,
       we need to fill in the members of the relevant structure TBrowseInfo}

      try
       with MyBrowseInfo do begin
         hwndOwner := Application.Handle;  // owner of dialog window
         pidlRoot := MyItemIDList;// specified the root folder
         pszDisplayName := shBuff;// this receives the selected folder
	 lpszTitle := Title;  	  // dialog title
         ulFlags := BIF_RETURNONLYFSDIRS; // return only file-system dirs
         if Success then begin

           {OK, this is the second part of selecting the initial directory
           of the browse dialog. lpfn points to a callback function, which
           the dialog window calls whenever events occur. One of the
           events is the opening of the dialog window. When this occurs
           we will send a selection message to browse dialog window,
           which will select the intial directory of our choice}

	   lpfn := BrowseCallbackProc;

           {lParam gets passed to the callback function. It represents
	   the item identifier (obtained above) of the directory we
           wish to select}

           lParam := Integer(SelectionIDList);
         end {if}
         else begin

           {If, for whatever reason we couldn't obtain item identifier
            we set the callback function to nil}

           lpfn := nil;
           lParam := 0;
         end;{else}
       end;{with}

       {Here is where the dialog is called up for display, finally!
       The return result is the item identifier for the directory
       which was chosen by the user}

       TheItemIDList := SHBrowseForFolder(MyBrowseInfo);
       try

        {Convert the item identfier into a directory name}

        if SHGetPathFromIDList(TheItemIDList, shBuff) then
           DestDir := shBuff
          else DestDir:='';  { added ... }
       finally

        {It is very important that free the item identfiers}

        MyShellMalloc.Free(TheItemIDList); // Clean-up
       end;{try/f}
      finally
       MyShellMalloc.Free(SelectionIDList); // Clean-up.
      end;{try/f}
     finally
      MyShellMalloc.Free(MyItemIDList); // Clean-up.
     end;{try/f}
    finally
     MyShellMalloc.Free(shBuff); // Clean-up.
    end;{try/f}
  end;{if}
  Result := {String(PChar(}DestDir{))};  // the result!!

  if (DestDir <> '') then InitDir:=DestDir;
end;


end.

