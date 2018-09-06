#ifndef glgame_h
#define glgame_h

#include <windows.h>		// Header File For Windows
#include <gl\gl.h>			// Header File For The OpenGL32 Library
#include <gl\glu.h>			// Header File For The OpenGL32 Library

#include "game.h"

extern int DrawGameScene(Game &);

extern bool DrawGameStats(Game& game);

extern bool glGameInit(void);
extern bool glGameDestroy(void);


#endif
