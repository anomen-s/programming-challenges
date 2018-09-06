#ifndef gltext_h
#define gltext_h

#include <windows.h>		// Header File For Windows
#include <gl\gl.h>			// Header File For The OpenGL32 Library
#include <stdarg.h>
#include <string>
//#include "globals.h"

extern void gltPrintf(const char *fmt, ...);
extern void gltPrint(const char *);
extern void gltPrint(const std::string &);
extern void glPrint(GLint x, GLint y, char *string, int set);

extern void gltInitFonts(void);
extern void gltDeleteFonts(void);


#endif