#ifndef glinit_h
#define glinit_h


#include <windows.h>		// Header File For Windows
#include <gl\gl.h>			// Header File For The OpenGL32 Library

extern bool CreateGLWindow(int width, int height, int bits);
extern void KillGLWindow(void);// Properly Kill The Window
extern void ResizeGLScene(GLsizei width, GLsizei height);// Resize And Initialize The GL Window


#endif
