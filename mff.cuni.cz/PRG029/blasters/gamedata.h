#ifndef gamedata_h
#define gamedata_h

#include <winsock.h>
#include <string>
#include <climits>
#include <vector>
#include <deque>
#include "globals.h"

enum CellType { 
    CELL_EMPTY, 
    CELL_WALL, 
    CELL_ROCK, 
    CELL_OUTSIDE, 
    CELL_BOMB, 
    CELL_ERROR };


// multiply float values by this const to avoid sending floats
#define STEP_PRECISION 1024.0f   

// default settings
#define DEFAULTBOMBTIMEOUT 2000
#define DEFAULTBOMBSTRENGTH 2
#define DEFAULTPLAYERSPEED (6.0f*UPDATEPERIOD/1000.0f)

#define GAMETIMELIMIT (3*60*1000) // three minute time limit

#define DIRECTION_VERT 0x02
#define DIRECTION_HORIZ 0x04

enum Direction { UP = 2, DOWN = 3, LEFT = 4, RIGHT = 5 }; // DON'T CHANGE THE ORDER !

struct Position {
    int x, y;
    Position(): x(0), y(0) {}
    Position(int px, int py): x(px), y(py) {}
//    Position(const Position &p): x(p.x), y(p.y) {}
    Position operator+(const Position &b) { return Position(this->x + b.x, this->y + b.y); }
    Position operator-(const Position &b) { return Position(this->x - b.x, this->y - b.y); }
    Position operator+(const int *a) { return Position(this->x + a[0], this->y + a[1]); }
    Position& operator+=(const Position &b) { x+= b.x;y+= b.y;return *this; }
    Position& operator+=(const int *a)  { x+= a[0];y+= a[1];return *this; }
    Position operator-(const int *a) { return Position(this->x - a[0], this->y - a[1]); }
    bool operator ==(const Position &b) { return ((b.x == this->x) && (b.y == this->y)); }
    bool operator !=(const Position &b) { return !(*this==b); }
    
    Position Forward(Direction dir) {
        Position d = *this;
        switch (dir) {
            case UP:    d.y += 1;break;
            case DOWN:  d.y -= 1;break;
            case LEFT:  d.x -= 1;break;
            case RIGHT: d.x += 1;break;
        }//switch
        return d;
    }//
    Position Backward(Direction dir) {
        Position d = *this;
        switch (dir) {
            case UP:    d.y -= 1;break;
            case DOWN:  d.y += 1;break;
            case LEFT:  d.x += 1;break;
            case RIGHT: d.x -= 1;break;
        }//switch
        return d;
    }//

};

typedef Position Size;


typedef unsigned int PID; // player ID  ; 1=local1 ; 2=local2

#define PID_MIN 200
#define PID_MAX (SHRT_MAX-2) // instead of (INT_MAX-2)


struct Bomb {
//    Bomb(): pos(0,0) {}
//    Bomb(const Bomb &src): pos(src.pos), time(src.time), owner(src.owner), strength(src.strength) {}
    Bomb(): pos(0,0), time(0), owner(0), strength(0) { }
    Bomb(PID o, Position p, int t, int s): pos(p), time(t), owner(o), strength(s) {}
    Position pos;
    int     data[6];
    DWORD   time;    // time of placement !!!
    PID     owner;
    int     strength;
};

typedef std::deque <Bomb> Bombs;


enum PowerUpType { 
    POWER_NOBOMB = 0,   // player cannot cast bombs (data = ms)
    POWER_STRENGTH = 1, // bombs +1 (data = str bonus = 1)
    POWER_BOMB = 2,     // one more bomb (data = # of bonus bombs = 1)
    POWER_SPEED = 3     // faster movement (data = bonus * STEP_PRECISION)
    //POWER_RANDOM = 4    // random powerup - must be last
    };
const int POWERUP_TYPES_COUNT = 4;

#define POWERUP_SPEEDBONUS 0.50f
#define POWERUP_NOBOMBDELAY 8000   // 8 seconds without bombs

struct PowerUp {
    PowerUpType type;
    Position pos;
//    int time;
    int data;
};

typedef std::deque <PowerUp> PowerUps;


#define LOCALPLAYER1 1 // don't change 
#define LOCALPLAYER2 2 // in globals.h is defined bitmask PLAYER_BIT = 3


struct ColorType {
  unsigned char rgb[3];
  ColorType() {}
  ColorType(unsigned char r_,unsigned char g_,unsigned char b_) { rgb[0]=r_;rgb[1]=g_;rgb[2]=b_; }
};


class Player 
{
public:
	enum PlayerType { 
		PT_ABSTRACT,
		PT_LOCAL1,	// local player
		PT_LOCAL2,	// local player
		PT_AI,		// computer
		PT_REMOTE	// remote
	};

    Player();
	Player(PlayerType type_, PID pid_, const char *name_ = "Unnamed", int score_ = 0); 
	PlayerType type() const;
	bool localControls() const;

	std::string name;
	ColorType color;
	Direction heading;
	int     getMaxBombs();
	void    setMaxBombs(int bombs);
	void    pickupPowerUp(const PowerUp &);
	void    newRound(int maxbombs, float px, float py);
	void    removePlayer(); // remove Connection object from gConnections
	bool    alive;
	int     score;
	bool	moving;
	bool    bombing;
	float   bonusspeed;
	int     bonusstrength;
	PID		pid;    // unique PID (allows reconnection)
	int     ping;
	float	px;     // x position
	float	py;     // y position
	Controls *pcontrols;
	virtual ~Player();
	int		cellposx(); // x position of cell
	int		cellposy(); // y position of cell
	Position cellpos(); // position of cell
//	PowerUps powerups;
//	int     availBombs();
private:
	SOCKET	s;
	int		maxbombs;
	DWORD   nobombtimeout; //picked up POWER_NOBOMB
	PlayerType ptype;
};

typedef std::vector <Player> Players;


#endif
