#ifndef blasters_h
#define blasters_h

#include <windows.h>		// Header File For Windows
#include "game.h"


#define SCREEN_BITS 32
#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 480

extern int ProcessMessages(int sleep = 0);
extern LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);	// Declaration For WndProc

// handler for menu item "Start game"
// executes RunGame
extern bool StartGame(int);
extern bool ServerGame(Game &);

// handler for menu item "join game"
// shows ip dialog and starts ClientGame
extern bool JoinGame(int);

extern bool ClientGame(Game &game);

extern bool GetPlayerName(int player);

extern bool Exit(int);

extern bool SetupControls(int keyid);


#endif
