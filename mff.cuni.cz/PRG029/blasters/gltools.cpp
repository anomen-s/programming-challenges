#include "gltools.h"

#include <gl\glu.h>			// Header File For The OpenGL32 Library

#include "gl/glpng.h"
#include "globals.h"
#include "keyb.h"
#include "logger.h"
#include "blasters.h"
#include "gltext.h"

#include <stdio.h>

using namespace std;

bool DrawGetStr(const char* prompt, const char* text)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	// Clear The Screen And The Depth Buffer
	glLoadIdentity();									// Reset The View

	glColor3f(1.0f,1.0f,0.0f);	
//	glRasterPos3f(-0.5f, 0.1f, -2);
	glLoadIdentity();
	glTranslated(-0.5*0.08*strlen(prompt), 0.2, 0);
	gltPrintf("%s", prompt);
//	glRasterPos3f(-0.5f, -0.1f, -2);
	glLoadIdentity();
	glTranslated(-0.04*strlen(text), -0.2, 0);
	glColor3f(1,1,1);
	gltPrintf("%s", text);

	return true;										// Keep Going
}

bool gltGetStr(const string prompt, string& text)
{
    clearKeyBuffer();
	bool done = false;
	unsigned char key;
	while (!done) {
		ProcessMessages();

		if (readkey(&key, KEYS_TEXTINPUT)) {
			text = text + (char)key;
		}
		if (testkey(VK_BACK) && (text.length() > 0)) { 
			text = text.substr(0,text.length()-1);
		}
		if (testkey(VK_RETURN)) { 
			done = true; 
		}

		if ((!DrawGetStr(prompt.c_str(), text.c_str())) || testkey(VK_ESCAPE))	// Active?  Was There A Quit Received?
		{
			return false;							// ESC or DrawGLScene Signalled A Quit
		} else {									// Not Time To Quit, Update Screen	
			SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
		}
	}//while
    clearKeyBuffer();
	return true;
}

bool gltMessageBox(string title, string text)
{
    clearKeyBuffer();

    glMatrixMode(GL_PROJECTION);						
	glLoadIdentity();									
	GLfloat aspect = 0.5f * (((GLfloat)globals.width / (GLfloat)globals.height) + 1.0f);
	if (globals.width > globals.height) {glOrtho(-aspect,aspect,-1,1,-5,5); }
	else { glOrtho(-1,1,-aspect,aspect,-5,5); }
	glMatrixMode(GL_MODELVIEW);							
	glLoadIdentity();									
    
    bool done = false;
	while (!done) {
		ProcessMessages();
		if (testkey(VK_RETURN)) { 
			done = true; 
		}
		if ((!DrawGetStr(title.c_str(), text.c_str())) || testkey(VK_ESCAPE))	// Active?  Was There A Quit Received?
		{
			return false;							// ESC or DrawGLScene Signalled A Quit
		} else {									// Not Time To Quit, Update Screen	
 	        glColor3f(0.7f,0.7f,0);	
    	    glLoadIdentity();									
            glTranslated(-1, -0.98f, 0.2);
            gltPrint("Press Enter to continue.");

			SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
		}
	}//while

    clearKeyBuffer();
    return true;
}

bool gltGetChar(string prompt, unsigned char& k)
{
	bool done = false;
	unsigned char key = k;
	string keycode;
	
	while (!done) {
		ProcessMessages();

		if (readkey(&key, KEYS_ALL)) {
		    done = true;
		    if (key != VK_ESCAPE) { 
			    k = key; 
			}//if
		}//if
		keycode = getKeyName(key);
		if (keycode.length() < 1) {
		    keycode = strprintf("#%u", unsigned int(key));
		}
		
		if (!DrawGetStr(prompt.c_str(), keycode.c_str()))	// Active?  Was There A Quit Received?
		{
			return 0;							// ESC or DrawGLScene Signalled A Quit
		} 
		else {									// Not Time To Quit, Update Screen	
			SwapBuffers(globals.hDC);			// Swap Buffers (Double Buffering)
		}
	}//while
	Sleep(500);
    clearKeyBuffer();
	return true;
}


GLuint loadtexture(const char *file)
{
	pngInfo info;
	GLuint t = 0;
    pngSetStencil(255, 255, 128); // for explosions
	glGenTextures(1, &t);
	glBindTexture(GL_TEXTURE_2D, t);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	if (pngLoad(file, PNG_NOMIPMAP, PNG_STENCIL, &info)) {
	    #ifdef _DEBUG
    	    logger->logf("%s: Size=%i,%i Depth=%i Alpha=%i", file, info.Width, info.Height, info.Depth, info.Alpha);
	    #endif
	}
	else {
	   logger->log("Can't load texture ", file);
	}
	return t;
}

