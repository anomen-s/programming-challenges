#ifndef game_h
#define game_h

#include <vector>
#include <string>
#include <stdarg.h>

#include "globals.h"
#include "gamedata.h"

//bomb explosion
//#define XTIMERBITS 8
//#define XTIMEROFFSET 0x0F
#define XTIMER (int(150/UPDATEPERIOD))

class Game {
public:
	Game(const char* host, unsigned int port);
	Game(int width, int height);
	int     getWidth() const;
	int     getHeight() const;
	bool    localGame() const;
	bool    playerControls();          // returns true if something;s changed
	int     remotePlayerControls();
	Players players;
//	void    setCurrentTimestamp();
//	DWORD   getCurrentTimeStamp();
	void    bombExplosion(Bomb &);
	int     playersBombs(PID);
	bool    updateGameState(bool sendPlayerPos = false); // returns false when game over
	bool    broadcastGameStateChange();
    bool    sendControlsToServer();     // returns result of write operation
	bool    recvGameState();
    bool    sendInitData(); // send game and players positions
    int     alivePlayers() const;
    Player& findByPID(PID);         // all players
//	void    setupServer(u_short port);
    CellType cell(int x, int y);
    CellType cell(const Position &p);
    CellType& boardcell(const Position &p);
    CellType& boardcell(int x, int y);
    void    init();
    bool    loadFromFile(std::string filename);
    void    recvBoard(const char* data, int width, int height);
    std::string  exportBoard(); // exports board data for recvBoard
    void    randomBoard(int nwalls, int npowerups); // % of walls & # of % of walls with powerup
    PID     newPID();
    int     timelimit;
    DWORD   gamestart;
    ~Game();
    Bombs   bombs;
    Bombs   xbombs;
    PowerUps powerups;
    std::string ghost; // remote computer name
	float   PLAYERSPEED;
	int     BOMBTIMEOUT;
	int     BOMBSTRENGTH;
private:
	int     gwidth;
	int     gheight;
	CellType *board;
	//int     time; -- use globals.getGameTimer()
	bool    glocal;
	void    movePlayer(Player &);
	bool    addGameStateChange(const char *fmt, ...);
	bool    clearGameStateChange();
    void    killPlayerByBomb(const Bomb &bomb, const Position& pos);
    Bombs::iterator bombAtPosition(const Position&); 
    Player& findByPosition(const Position&); // only alive players
	std::string  gamestatepacket;
	Player  dummy;
};

#endif
