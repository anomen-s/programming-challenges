#ifndef gltools_h
#define gltools_h

#include <windows.h>		// Header File For Windows
#include <gl\gl.h>			// Header File For The OpenGL32 Library
#include <string>

// display dialog for string input
// returns true if successful, false else (eg: user pressed ESCAPE)
extern bool gltGetStr(const std::string prompt, std::string& text);

// display dialog for single string input
// returns true if successful, false else (eg: user pressed ESCAPE)
extern bool gltGetChar(std::string prompt, unsigned char& k);

// returns true if user pressed Enter
//         false if user pressed Escape
extern bool gltMessageBox(std::string title, std::string text); 

extern GLuint loadtexture(const char *file);

#endif
