#ifndef globals_h
#define globals_h

#include <windows.h>
#include <string>
#include <stdarg.h>

// game state update cycle length in ms
#define UPDATEPERIOD 28


#define PI  3.14159265359

// displays error dialog and sends msg to logger
extern void errorMsg(char *msg);

// round float to integer
extern int ftoi(float f);

// round float to long integer
extern long ftol(float f);

// modification of sprintf for std::string
extern std::string strprintf(const char *fmt, ...);

// removes & returns first line from given string
//std::string strtokline(std::string &);

// returns first word
//std::string strfirstword(const std::string);

// returns first word and fills argv array with
// integer values from given string
//std::string strparsecommand(const std::string, int maxargc, int* argv);

// returns first word of given string and fills buffer
// with remaining characters from given string
//std::string strparsecommand(const std::string, std::string &buffer);


#define SOUND_EXPLOSION 0
#define SOUND_BEEP 1
//number of defined sounds
#define SOUNDS_COUNT 2

extern bool SoundInit();
extern void SoundFinish();
extern bool playSound(int sound);




#define KEY_LEFT 0
#define KEY_RIGHT 1
#define KEY_UP 2
#define KEY_DOWN 3
#define KEY_FIRE 4

#define KEY_BIT(key) (4 << key)
#define PLAYER_BIT 3  // player codes are 1 & 2 (LOCALPLAYER1, LOCALPLAYER2)

union Controls {
	unsigned char c[6];
	struct {
		unsigned char left, right, up, down, fire; 
	};
};


class Globals {
public:

	void initGlobals()
	{
		hDC = NULL;
		hRC = NULL;
		hWnd = NULL;
		active = true;
		gamemode = false;
		fullscreen= true;
		memset(keys, 0, sizeof(keys));
   		hInstance = GetModuleHandle(NULL);				// Grab An Instance For Our Window
		player1 = "player1";
		player2 = "player2";
		mousex = 0;
		mousey = 0;
		timer = GetTickCount();
        static char defcontrols1[] = { VK_LEFT, VK_RIGHT, VK_UP, VK_DOWN, VK_RETURN, 0};
        static char defcontrols2[] = { 'A', 'D', 'W', 'S', VK_SPACE, 0};
		memcpy(p1controls.c, defcontrols1, sizeof(defcontrols1));
		memcpy(p2controls.c, defcontrols2, sizeof(defcontrols2));
		defaultPort = 15790;
	}

    inline DWORD getGameTimer() 
    {
        return timer;
    }
    
    bool updateGameTimer() // updates game timer. returns true whet cycle time elapsed
    {
		if (GetTickCount() > (timer + UPDATEPERIOD)) {
            timer = GetTickCount();
            return true;
        }//if
        return false;
    }


	HDC			hDC;	// Private GDI Device Context
	HGLRC		hRC;	// Permanent Rendering Context
	HWND		hWnd;	// Holds Our Window Handle
	HINSTANCE	hInstance;// Holds The Instance Of The Application


	bool	keys[256];	// Array Used For The Keyboard Routine
	int		mousex, mousey;
	bool	active;		// Window Active Flag Set To TRUE By Default
	bool	gamemode;	
	bool	fullscreen;	// Fullscreen Flag Set To Fullscreen Mode By Default

	int		width;		// screen
	int		height;
	int		bitsperpixel;

	std::string	player1;	// player names
	std::string player2;
	Controls p1controls;
	Controls p2controls;

	int defaultPort;
private:
	DWORD	timer;      // last gamestate update

};

extern Globals globals;


#endif
