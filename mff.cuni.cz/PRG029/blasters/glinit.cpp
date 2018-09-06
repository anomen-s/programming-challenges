#include <windows.h>
#include <gl\glu.h>	
#include "gl\glpng.h"

#include "blasters.h"
#include "globals.h"
#include "glinit.h"

static char wcname[] = "OpenGLblasters";
static char wctitle[] = "Blasters";

extern bool InitGL();		// All Setup For OpenGL Goes Here

#ifndef	CDS_FULLSCREEN		// CDS_FULLSCREEN Is Not Defined By Some
 #define CDS_FULLSCREEN 4	// Compilers. By Defining It This Way,
#endif				// We Can Avoid Errors


/*	This Code Creates Our OpenGL Window.  Parameters Are:					*
 *	width			- Width Of The GL Window Or Fullscreen Mode				*
 *	height			- Height Of The GL Window Or Fullscreen Mode			*
 *	bits			- Number Of Bits To Use For Color (8/16/24/32)			*/

bool CreateGLWindow(int width, int height, int bits)
{
	GLuint		PixelFormat;			// Holds The Results After Searching For A Match
	WNDCLASS	wc;						// Windows Class Structure
	DWORD		dwExStyle;				// Window Extended Style
	DWORD		dwStyle;				// Window Style
	RECT		WindowRect;				// Grabs Rectangle Upper Left / Lower Right Values
	WindowRect.left=(long)0;			// Set Left Value To 0
	WindowRect.right=(long)width;		// Set Right Value To Requested Width
	WindowRect.top=(long)0;				// Set Top Value To 0
	WindowRect.bottom=(long)height;		// Set Bottom Value To Requested Height
	globals.width=width;
	globals.height=height;

	wc.style			= CS_HREDRAW | CS_VREDRAW | CS_OWNDC;	// Redraw On Size, And Own DC For Window.
	wc.lpfnWndProc		= (WNDPROC) WndProc;					// WndProc Handles Messages
	wc.cbClsExtra		= 0;									// No Extra Window Data
	wc.cbWndExtra		= 0;									// No Extra Window Data
	wc.hInstance		= globals.hInstance;					// Set The Instance
	wc.hIcon			= LoadIcon(NULL, IDI_WINLOGO);			// Load The Default Icon
	wc.hCursor			= LoadCursor(NULL, IDC_ARROW);			// Load The Arrow Pointer
	wc.hbrBackground	= NULL;									// No Background Required For GL
	wc.lpszMenuName		= NULL;									// We Don't Want A Menu
	wc.lpszClassName	= wcname;								// Set The Class Name

	if (!RegisterClass(&wc))									// Attempt To Register The Window Class
	{
		errorMsg("Failed To Register The Window Class.");
		return false;											// Return FALSE
	}//if
	
	if (globals.fullscreen)									// Attempt Fullscreen Mode?
	{
		DEVMODE dmScreenSettings;								// Device Mode
		memset(&dmScreenSettings,0,sizeof(dmScreenSettings));	// Makes Sure Memory's Cleared
		dmScreenSettings.dmSize=sizeof(dmScreenSettings);		// Size Of The Devmode Structure
		dmScreenSettings.dmPelsWidth	= width;				// Selected Screen Width
		dmScreenSettings.dmPelsHeight	= height;				// Selected Screen Height
		dmScreenSettings.dmBitsPerPel	= bits;					// Selected Bits Per Pixel
		dmScreenSettings.dmFields=DM_BITSPERPEL|DM_PELSWIDTH|DM_PELSHEIGHT;

		// Try To Set Selected Mode And Get Results.  NOTE: CDS_FULLSCREEN Gets Rid Of Start Bar.
		if (ChangeDisplaySettings(&dmScreenSettings,CDS_FULLSCREEN)!=DISP_CHANGE_SUCCESSFUL)
		{
			// If The Mode Fails, Offer Two Options.  Quit Or Use Windowed Mode.
			if (MessageBox(NULL,"The Requested Fullscreen Mode Is Not Supported By\nYour Video Card. Use Windowed Mode Instead?","Blasters",MB_YESNO|MB_ICONEXCLAMATION)==IDYES)
			{
				globals.fullscreen=false;	// Windowed Mode Selected.  Fullscreen = FALSE
			}
			else {
				// Pop Up A Message Box Letting User Know The Program Is Closing.
				errorMsg("Program Will Now Close.");
				return false;									// Return FALSE
			}
		}//if
	}//if

	if (globals.fullscreen)									// Are We Still In Fullscreen Mode?
	{
		dwExStyle=WS_EX_APPWINDOW;								// Window Extended Style
		dwStyle=WS_POPUP;										// Windows Style
		ShowCursor(FALSE);										// Hide Mouse Pointer
	}
	else {
		dwExStyle=WS_EX_APPWINDOW | WS_EX_WINDOWEDGE;			// Window Extended Style
		dwStyle=WS_OVERLAPPEDWINDOW;							// Windows Style
	}

	AdjustWindowRectEx(&WindowRect, dwStyle, FALSE, dwExStyle);		// Adjust Window To True Requested Size

	// Create The Window
	if (!(globals.hWnd=CreateWindowEx(dwExStyle,							// Extended Style For The Window
								wcname,							// Class Name
								wctitle,							// Window Title
								dwStyle |							// Defined Window Style
								WS_CLIPSIBLINGS | WS_CLIPCHILDREN,	// Required Window Style
								0, 0,								// Window Position
								WindowRect.right-WindowRect.left,	// Calculate Window Width
								WindowRect.bottom-WindowRect.top,	// Calculate Window Height
								NULL,								// No Parent Window
								NULL,								// No Menu
								globals.hInstance,					// Instance
								NULL)))								// Don't Pass Anything To WM_CREATE
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Window Creation Error.");
		return false;								// Return FALSE
	}

	static PIXELFORMATDESCRIPTOR pfd=				// pfd Tells Windows How We Want Things To Be
	{
		sizeof(PIXELFORMATDESCRIPTOR),				// Size Of This Pixel Format Descriptor
		1,											// Version Number
		PFD_DRAW_TO_WINDOW |						// Format Must Support Window
		PFD_SUPPORT_OPENGL |						// Format Must Support OpenGL
		PFD_DOUBLEBUFFER,							// Must Support Double Buffering
		PFD_TYPE_RGBA,								// Request An RGBA Format
		bits,										// Select Our Color Depth
		0, 0, 0, 0, 0, 0,							// Color Bits Ignored
		0,											// No Alpha Buffer
		0,											// Shift Bit Ignored
		0,											// No Accumulation Buffer
		0, 0, 0, 0,									// Accumulation Bits Ignored
		16,											// 16Bit Z-Buffer (Depth Buffer)  
		0,											// No Stencil Buffer
		0,											// No Auxiliary Buffer
		PFD_MAIN_PLANE,								// Main Drawing Layer
		0,											// Reserved
		0, 0, 0										// Layer Masks Ignored
	};
	
	if (!(globals.hDC=GetDC(globals.hWnd)))							// Did We Get A Device Context?
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Can't Create A GL Device Context.");
		return FALSE;								// Return FALSE
	}

	if (!(PixelFormat=ChoosePixelFormat(globals.hDC, &pfd)))	// Did Windows Find A Matching Pixel Format?
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Can't Find A Suitable PixelFormat.");
		return FALSE;								// Return FALSE
	}

	if(!SetPixelFormat(globals.hDC,PixelFormat,&pfd))// Are We Able To Set The Pixel Format?
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Can't Set The PixelFormat.");
		return FALSE;								// Return FALSE
	}

	if (!(globals.hRC = wglCreateContext(globals.hDC)))// Are We Able To Get A Rendering Context?
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Can't Create A GL Rendering Context.");
		return FALSE;								// Return FALSE
	}

	if(!wglMakeCurrent(globals.hDC,globals.hRC))					// Try To Activate The Rendering Context
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Can't Activate The GL Rendering Context.");
		return FALSE;								// Return FALSE
	}

	ShowWindow(globals.hWnd, SW_SHOW);						// Show The Window
	SetForegroundWindow(globals.hWnd);						// Slightly Higher Priority
	SetFocus(globals.hWnd);									// Sets Keyboard Focus To The Window
	ResizeGLScene(width, height);					// Set Up Our Perspective GL Screen

	if (!InitGL())									// Initialize Our Newly Created GL Window
	{
		KillGLWindow();								// Reset The Display
		errorMsg("Initialization Failed.");
		return FALSE;								// Return FALSE
	}

	return true;									// Success
}


bool InitGL()										// All Setup For OpenGL Goes Here
{
	glEnable(GL_TEXTURE_2D);							// Enable Texture Mapping
	glShadeModel(GL_SMOOTH);							// Enable Smooth Shading
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);				// Black Background
	glClearDepth(1.0f);									// Depth Buffer Setup
	glEnable(GL_DEPTH_TEST);							// Enables Depth Testing
	glDepthFunc(GL_LEQUAL);								// The Type Of Depth Testing To Do
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);	// Really Nice Perspective Calculations

	return TRUE;										// Initialization Went OK
}


void KillGLWindow()								// Properly Kill The Window
{

	if (globals.fullscreen)							// Are We In Fullscreen Mode?
	{
		ChangeDisplaySettings(NULL,0);					// If So Switch Back To The Desktop
		ShowCursor(true);								// Show Mouse Pointer
	}

	if (globals.hRC)									// Do We Have A Rendering Context?
	{
		if (!wglMakeCurrent(NULL, NULL))				// Are We Able To Release The DC And RC Contexts?
		{
			errorMsg("Release Of DC And RC Failed.");
		}

		if (!wglDeleteContext(globals.hRC))			// Are We Able To Delete The RC?
		{
			errorMsg("Release Rendering Context Failed.");
		}
		globals.hRC=NULL;										// Set RC To NULL
	}

	if (globals.hDC && !ReleaseDC(globals.hWnd,globals.hDC))	// Are We Able To Release The DC
	{
		errorMsg("Release Device Context Failed.");
		globals.hDC=NULL;								// Set DC To NULL
	}

	if (globals.hWnd && !DestroyWindow(globals.hWnd))		// Are We Able To Destroy The Window?
	{
		errorMsg("Could Not Release hWnd.");
		globals.hWnd=NULL;								// Set hWnd To NULL
	}

	if (!UnregisterClass(wcname,globals.hInstance))	// Are We Able To Unregister Class
	{
		errorMsg("Could Not Unregister Class.");
		globals.hInstance=NULL;									// Set hInstance To NULL
	}
}


void ResizeGLScene(GLsizei width, GLsizei height)		// Resize And Initialize The GL Window
{
	if (height==0)										// Prevent A Divide By Zero By
	{
		height=1;										// Making Height Equal One
	}

	glViewport(0,0,width,height);						// Reset The Current Viewport

	glMatrixMode(GL_PROJECTION);						// Select The Projection Matrix
	glLoadIdentity();									// Reset The Projection Matrix

	// Calculate The Aspect Ratio Of The Window
//	gluPerspective(45.0f,(GLfloat)width/(GLfloat)height,0.1f,100.0f);
/*	GLfloat aspect = 0.5f * (((GLfloat)width / (GLfloat)height) + 1.0f);
	if (width > height) {
		glOrtho(-aspect,aspect,-1,1,-5,5);
	} else {
		glOrtho(-1,1,-aspect,aspect,-5,5);
	}*/

	glMatrixMode(GL_MODELVIEW);							// Select The Modelview Matrix
	glLoadIdentity();									// Reset The Modelview Matrix
}
