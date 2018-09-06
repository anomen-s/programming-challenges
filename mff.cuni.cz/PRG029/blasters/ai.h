#ifndef ai_h
#define ai_h

#include "game.h"
#include "gamedata.h"

extern bool aiInit();
extern const char* aiPlayerName(Game& game);
extern bool aiControl(Game& game);


#endif
