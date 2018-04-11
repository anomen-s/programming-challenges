<readme>
<title>SML File Viewer</title>
<subtitle>Correspondence stage solution of ICP'2000</subtitle>
<para>---------------------------------------------------------------------</para>
<h3><link>help.sml</link>User's Guide</h3>
<para>---------------------------------------------------------------------</para>
<h3>Notes:</h3>

<para># Program dosn't support HTTP (I'm sorry).</para>
<para># This project was successfuly compiled in both Delphi 3 and Delphi 5.</para>
<para># Configuration informations are stored in registry key HKEY_CURRENT_USER\Software\PTN\SMLviewer</para>
<para># Any similarity with existing internet browser is purely coincidental. <smile>:-)</smile></para>
<para>---------------------------------------------------------------------</para>
<h3>List of files of project:</h3>

<li>About</li>
<para>	TAboutForm - Form 'About'</para>
<li>Config</li>
<para>	TConfigForm - Form 'Options'</para>
<li>Display</li>
<para>	TDisplayThread - thread which paints document on the main form</para>
<li>DocUnit</li>
<para>	TDocument - object for loading and translating .sml files</para>
<li>FStream</li>
<para>	TDocumentStream - base class for objects TDocument and TStyleLoader</para>
<li>hdr.inc</li>
<para>	header file with compiler directives</para>
<li>ICP2000</li>
<para>	main project file</para>
<li>MainUnit</li>
<para>	TMainForm - main form</para>
<li>Styles</li>
<para>	TStyleLoader - object for reading style files</para>
<li>ICP2000.EXE</li>
<para>	stand-alone program compiled in Delphi 3 C/S (without runtime packages)</para>
<para>---------------------------------------------------------------------</para>
<h3>Some basic mechanisms:</h3>
<p># When you try to somehow open file, program always calls TMainUnit.OpenDocument,
which calls constructor TDocument.OpenFile (<path>docunit.pas</path>), which does all the work - looks for
style file, loads it by calling LoadStyles (<path>styles.pas</path>) and parses the document.
Then OpenDocument sets variables in record TCtrl (<path>display.pas</path>)
to control the thread (TDisplayThread) which provides the displaying of document
onto TMainForm.
</p>
<p> # Brief description of TDisplayThread (<path>display.pas</path>):</p>
<p>
~Main method Execute reads values from TCtrl record and calls appropriate methods(such as Draw).</p>
<p>
~Method Draw goes through the document and for every paragraph calls PaintPara.</p>
<p>~Method PaintPara calls PaintPicture / GetPictureSize for images,
and simple repeat cycle manages dispaying of text
(methods PaintTextLine and TextHeight)
</p>
<para>---------------------------------------------------------------------</para>
<author><black>Author:</black>xxxxxxx</author>

<author><black>email:</black>xxxxxx@xxxxx.xx</author>

</readme>
