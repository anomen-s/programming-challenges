#include <stdlib.h>
#include <windows.h>
#include <math.h>
#include <fstream>
#include <sstream>

#include "game.h"
#include "glgame.h"
#include "gltools.h"
#include "globals.h"
#include "keyb.h"
#include "logger.h"
#include "net.h"

using namespace std;

Game::Game(int width, int height)
{
	gwidth = width;
	gheight = height;
	glocal = true;
	ghost = "Local game";
	board = new CellType[height*width];
    timelimit = GAMETIMELIMIT;
}

Game::Game(const char* host, unsigned int port) 
{
    ConnectToServer(host, port);
	glocal = false;
	ghost = host;
	board = NULL;
}

const ColorType Colors[] = { 
    ColorType(255,0,0),
    ColorType(0,255,0),
    ColorType(255,255,0),     
    ColorType(0,0,255),
    ColorType(255,0,255)     
};

void Game::init()
{
	PLAYERSPEED = DEFAULTPLAYERSPEED;
	BOMBTIMEOUT = DEFAULTBOMBTIMEOUT;
	BOMBSTRENGTH = DEFAULTBOMBSTRENGTH;
	
    int i = 0;
    for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        p->newRound(
            2,
            float(((i&1) ^ (i>>1)) * (gwidth-1)),
            float((i&1) * (gheight-1)) //TODO: better player placement
        );
        p->color = Colors[i];
        i++;
        //p->score = 0;  do not change players score !
    }
    powerups.clear();
    bombs.clear();  // should be unnecessary
    xbombs.clear(); // should be unnecessary
    timelimit = 0;
    gamestart = globals.getGameTimer();
    // change players maxbombs,x,y,heading,moving
    //setup game - proj. matrix, load map
}

void Game::recvBoard(const char* data, int width, int height) 
{
    if (board != NULL) {
        delete[] board;
    }//if
	board = new CellType[height*width];
	gwidth = width;
	gheight = height;
	PowerUp pu;
	for (int y = 0; y < height; y++) {
    	for (int x = 0; x < width; x++) {
    	    pu.pos = Position(x,y);
            boardcell(x,y) = CELL_WALL; //default walue
	        switch (data[y*width+x]) {
	        case 'w':
	            //boardcell(x,y) = CELL_WALL;
	            break;
	        case 'x':
	            boardcell(x,y) = CELL_ROCK;
	            break;
	        case 'e':
	            boardcell(x,y) = CELL_EMPTY;
	            break;
	        case 'N':
	            pu.type=POWER_NOBOMB;
	            pu.data = POWERUP_NOBOMBDELAY;
	            powerups.push_back(pu);
	            break;
	        case 'S':
	            pu.type = POWER_STRENGTH;
	            pu.data = 1;
	            powerups.push_back(pu);
	            break;
	        case 'B':
	            pu.type = POWER_BOMB;
	            pu.data = 1;
	            powerups.push_back(pu);
	            break;
	        case 'F':
	            pu.type = POWER_SPEED;
	            pu.data = int(POWERUP_SPEEDBONUS * STEP_PRECISION);
	            powerups.push_back(pu);
	            break;
	        }//switch
	    }//for
	}//for
}

// exports current board. client loads it using recvBoard
string Game::exportBoard() 
{
    string buffer = "";
    string ctype = "w";
    Position pos;
    PowerUps::iterator pi; // in VC 6.0 vars cannot be declared inside case
    for (int y = 0; y < gheight;y++) {
	    for (int x = 0; x < gwidth;x++) {
	        pos = Position(x,y);
	        switch (boardcell(x,y)) {
	        case CELL_EMPTY:
	            buffer.append("e");
	            break;
	        case CELL_WALL:
	            ctype = "w";
	            for (pi = powerups.begin(); pi != powerups.end(); ++pi) {
	                if (pi->pos == pos) {
	                    switch (pi->type) {
	                        case POWER_NOBOMB:
	                        ctype = "N";break;
	                        case POWER_STRENGTH:
	                        ctype = "S";break;
	                        case POWER_BOMB:
	                        ctype = "B";break;
	                        case POWER_SPEED:
	                        ctype = "F";break;
	                    }//switch
	                    break;//for
	                }//if
	            }//for
	            buffer.append(ctype);
	            break;
	        case CELL_ROCK:
	            buffer.append("x");
	            break;
	        }//switch
	    }//for
	}//for
	return buffer;
}

bool marginalcell(const Position &p, int width, int height)
{
    if (((p.x==0)||(p.x==(width-1))) && ((p.y<=1)||(p.y>=(height-2)))) { 
        return true; 
    }
    if (((p.y==0)||(p.y==(height-1))) && ((p.x<=1)||(p.x>=(width-2)))) { 
        return true; 
    }
    return false;
}

void Game::randomBoard(int nwalls, int npowerups)
{
    for (int x = 0; x < gwidth; x++) {
        for (int y = 0; y < gheight; y++) {
            if (((x&1)==1)&&((y&1)==1)) {
                boardcell(x,y) = CELL_ROCK;
            } else {
                boardcell(x,y) = CELL_EMPTY;
            }//if/else
        }//for
    }//for

    int maxrounds = 0;
    int placedpowerups = 0;
    int wmax = int(float(gheight*gwidth*nwalls) / 100);
    int pumax = int((npowerups * wmax) / 100);
    for (int i = 0; i < wmax; maxrounds++) {
        Position p(rand() % gwidth, rand() % gheight);
        CellType& cell = boardcell(p);
        if ((cell == CELL_EMPTY) && (!marginalcell(p, gwidth, gheight))) { 
            cell = CELL_WALL;
            i++; //number of created walls
            if (i <= pumax) {
                PowerUp pup;
                pup.type = PowerUpType(rand() % POWERUP_TYPES_COUNT);
                pup.pos = p;
                switch (pup.type) {
                    case POWER_SPEED:
                        pup.data = int((PLAYERSPEED * POWERUP_SPEEDBONUS) * STEP_PRECISION);
                        break;
                    case POWER_STRENGTH:
                        pup.data = 1;
                        break;
                    case POWER_BOMB:
                        pup.data = 1;
                        break;
                    case POWER_NOBOMB:
                        pup.data = POWERUP_NOBOMBDELAY; 
                        break;
                } //switch
                powerups.push_back(pup);
            }//if  
        }//if
        if (maxrounds > 10000) {
            logger->log("too many cycles in Game::randomBoard()");
            break;
        }//if
    }//for
}

bool Game::loadFromFile(std::string filename)
{
    ifstream f;
    string s;
    f.open(filename.c_str(), ios::in);
   	while (!f.eof()) {
		getline(f, s);
		istringstream istr;
		istr.rdbuf()->str(s);
		// parse input
	}
    return true;
}


Game::~Game() 
{
    if (board != NULL) { delete[] board; }
    CloseGameConnections();
}

/*void Game::setCurrentTimestamp()  --moved to globals
{
    time = GetTickCount();
}
DWORD Game::getCurrentTimeStamp()
{
    return time;
}*/

PID Game::newPID()
{
    bool ok = false;
    PID newpid = 0;
    while (!ok) {
        newpid = (int)(PID_MIN+((float(rand())/float(RAND_MAX))*(PID_MAX-PID_MIN)));
        ok = true;
        for (Players::iterator p = players.begin(); p != players.end(); ++p) {
            if (p->pid == newpid) { ok = false; }
        }//for
    }
    return newpid;
}


int Game::getWidth()  const
{
	return gwidth; 
} 
int Game::getHeight() const
{ 
	return gheight; 
}

CellType Game::cell(int x, int y)
{
    if ((x < 0) || (y < 0) || (x >= getWidth()) || (y >= getHeight())) {
        return CELL_OUTSIDE;
    }//if
    for (Bombs::const_iterator b = bombs.begin(); b != bombs.end(); ++b) {
     if ((b->pos.x == x) && (b->pos.y == y)) {
        return CELL_BOMB;
     }//if
    }//for
/*    if ((x&1) && (y&1)) {
        return CELL_ROCK;
    } //if*/
    return boardcell(x, y);
//    return CELL_ERROR;
}
CellType Game::cell(const Position &p)
{
    return cell(p.x, p.y);
}

CellType& Game::boardcell(const Position &p)
{
    return boardcell(p.x,p.y);
}
CellType& Game::boardcell(int x, int y)
{
    if ((x < 0) || (y < 0) || (x >= getWidth()) || (y >= getHeight())) {
        return board[0];
    }//if
    return board[gwidth*y + x];
}

int Game::playersBombs(PID player)
{
    int r = 0;
    for (Bombs::iterator b = bombs.begin(); b != bombs.end(); ++b) {
        if (b->owner == player) { r++; }
    } //for
    return r;
}

int Game::alivePlayers() const
{
    int r = 0;
    for (Players::const_iterator p = players.begin(); p != players.end(); ++p) {
        if (p->alive) { r++; }
    }//for
    return r;
}

Player& Game::findByPID(PID player)
{
    for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        if (p->pid == player) { return *p; }
    }//for
    logger->log("Couldn't find player ", (int) player);
    return dummy;
}

Player& Game::findByPosition(const Position& pos)
{
    for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        if ((p->alive) && (p->cellpos() == pos)) { return *p; }
    }//for
    return dummy;
}

Bombs::iterator Game::bombAtPosition(const Position& p) // all players
{
    for (Bombs::iterator b = bombs.begin(); b != bombs.end(); ++b) {
        if (b->pos == p) { break; }
    } //for
    return b;
    
}

bool Game::localGame() const
{ 
	return glocal; 
}

bool Game::addGameStateChange(const char *fmt, ...)
{
	char text[256];
	va_list ap;
	if (fmt == NULL) { return false; }
	va_start(ap, fmt);
	vsprintf(text, fmt, ap);
	va_end(ap);
	strcat(text, " \r\n");
    gamestatepacket.append(string(text));
    return true;
}

bool Game::broadcastGameStateChange() 
{
    bool result = true;
    if (!gamestatepacket.empty()) {
        #ifdef LOCALDEBUG
            logger->log("PACKET: ", gamestatepacket.c_str());
        #else
            result = SendToClients(gamestatepacket.c_str());
        #endif    
    }//if
    clearGameStateChange();
    return result;
}

bool Game::clearGameStateChange()
{
    gamestatepacket = "";
    return true;
}

static int directions[6][2] = { {0,0}, {0,0}, {0,1}, {0,-1}, {-1,0}, {1,0} };


void Game::movePlayer(Player &p)
{
    float pspeed = PLAYERSPEED + p.bonusspeed;
    Position c = p.cellpos();
    if (p.heading & DIRECTION_HORIZ) { // horiz
        if (cell(c+directions[p.heading]) == CELL_EMPTY) { // can move
            float toCenter = (float) fabs(p.py - c.y);
            if (p.py > c.y) {  // above center of cell
                p.py -= min(toCenter, pspeed);
            } else {
                p.py += min(toCenter, pspeed);
            }//if/else
            if (toCenter > pspeed) { 
                if (p.py > c.y) { // still above center of cell
                   p.heading = DOWN;
                } else {
                   p.heading = UP;
                }//if/else
            } else { // go to expected direction
                float toForward = (pspeed - toCenter);
                p.px += (directions[p.heading][0] * toForward);
            }//if
        } else { // can not move
            float toCenterX = min((float)fabs(p.px - c.x),pspeed);
            if (p.px > c.x ) { p.px -= toCenterX; } else { p.px += toCenterX; }
        }//if/else

    } else {  // VERTICAL MOVEMENT

        if (cell(c+directions[p.heading]) == CELL_EMPTY) { // can move
            float toCenter = (float)fabs(p.px - c.x);
            if (p.px > c.x) {  // above center of cell
                p.px -= min(toCenter, pspeed);
            } else {
                p.px += min(toCenter, pspeed);
            }//if/else
            if (toCenter > pspeed) { 
                if (p.px > c.x) { // still above center of cell
                   p.heading = LEFT;
                } else {
                   p.heading = RIGHT;
                }//if/else
            } else { // go to expected direction
                float toForward = (pspeed - toCenter);
                p.py += (directions[p.heading][1] * toForward);
            }//if
        } else {
            float toCenterY = min((float)fabs(p.py - c.y),pspeed);
            if (p.py > c.y ) { p.py -= toCenterY; } else { p.py += toCenterY; }
        }//if/else

    }//if/else
}

// update player state from keyboard control
// returns true if something's changed
bool Game::playerControls()
{
    bool result = false;

	for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        if (p->localControls()) {  // if PT_LOCAL1 or PT_LOCAL2

            bool m = p->moving;     // save current state
            bool b = p->bombing;
            Direction h = p->heading;

            p->moving = false;      // update state
            if (peekkey(p->pcontrols->left))  { p->heading = LEFT;  p->moving = true; }
			if (peekkey(p->pcontrols->right)) { p->heading = RIGHT; p->moving = true; }
			if (peekkey(p->pcontrols->up))    { p->heading = UP;    p->moving = true; }
			if (peekkey(p->pcontrols->down))  { p->heading = DOWN;  p->moving = true; }
			p->bombing = peekkey(p->pcontrols->fire);

            if ((m != p->moving) || (b != p->bombing) || (h != p->heading)) {
                result = true;
            }//if
		}//if
	}//for
	return result;
}

//update player state from inet packet
int Game::remotePlayerControls()
{
    CommandStruct cmd;
	for (Players::iterator p = players.begin(); p != players.end();) {
	    bool gotoNext = true;
		if (p->type() == Player::PT_REMOTE) {
		    while (readCommandFromPlayer(p->pid, cmd)) {
		        if (cmd.cmd == COMMAND_PLAYERCONTROL) {
		            p->heading = (Direction)cmd.intparams[0];
		            p->moving = (cmd.intparams[1] != 0);
		            p->bombing = (cmd.intparams[2] != 0);
		        }//if
		        else if (cmd.cmd == COMMAND_EXIT) {
                    p->removePlayer();
                    p = players.erase(p);
                    gotoNext = false;
		        }//if
		        else if (cmd.cmd == COMMAND_PING) {
		            string ping = COMMAND_PONG " ";
		            ping.append(cmd.strparam);
		            ping.append(" \r\n");
		            SendToClients(ping.c_str());
		        }//if
		        else
		            logger->log("Unknown command from client: ", cmd.cmd);
		    }//while
		}//if
        if (gotoNext) { ++p; }
    }//for
    return true;
}

void Game::killPlayerByBomb(const Bomb &bomb, const Position& pos)
{
    for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        if ((p->alive) && (p->cellpos() == pos)) { 
            p->alive = false;
            Player &bomber = findByPID(bomb.owner);
            if (bomber.pid != p->pid) {
                bomber.score++;
            } else {
                bomber.score--;
            }
    	    addGameStateChange(COMMAND_DEATH " %i", (int)p->pid);
    	    addGameStateChange(COMMAND_SCORE " %i %i", (int)bomber.pid, (int)bomber.score);
    	}//if
    }//for
}

void Game::bombExplosion(Bomb &bomb)
{
    addGameStateChange(COMMAND_EXPLODE " %i %i", (int)bomb.pos.x, (int)bomb.pos.y);

    playSound(SOUND_EXPLOSION);

    for (int i = 0; i <= 6; i++) { bomb.data[i] = bomb.strength; }
    bomb.data[0] = 0;
    
    Position bpos = bomb.pos;
    if (glocal) { killPlayerByBomb(bomb, bpos); }// is player standing over bomb ?
    for (int d = UP; d <= RIGHT; d++) {
        bpos = bomb.pos;
        for (int i = 1; i <= bomb.strength; i++) {
            bpos += directions[d];
            if (cell(bpos) == CELL_OUTSIDE) // outside
            { 
                bomb.data[d] = min(bomb.data[d], i-1);
                break; 
            }
            else if (cell(bpos) == CELL_ROCK) // rock
            { 
                bomb.data[d] = min(bomb.data[d], i-1);
                break; 
            }
            else if (cell(bpos) == CELL_WALL) //wall
            {
                bomb.data[d] = min(bomb.data[d], i);
                boardcell(bpos) = CELL_EMPTY;
                break; 
            }
            else /*if (glocal)*/ {   // empty cell - check for powerup & bombs & players (only on server)
                for (Bombs::iterator b = bombs.begin(); b != bombs.end(); ++b) {
                    if (b->pos == bpos) {
                        //bombExplosion(*b); // no. use forced premature explosion instead.
                        b->time = (globals.getGameTimer() - BOMBTIMEOUT + 1); // forced explosion, but delayed by one game cycle
                        break;
                    }//if
                }//for bombs
                for (PowerUps::iterator pu = powerups.begin(); pu != powerups.end(); ++pu) {
                    if (pu->pos == bpos) {
                        addGameStateChange(COMMAND_POWERUPDESTROY " %i %i", (int)pu->pos.x, (int)pu->pos.y);
                        pu = powerups.erase(pu);
                        break;
                    }//if
                }//for bombs
                if (glocal) { killPlayerByBomb(bomb, bpos); }
    
            }//else if

        }//for cells
    }//for directions
}

bool Game::sendControlsToServer()
{
    static 
    string buffer;
    clearGameStateChange();
    for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        if ((p->type() == Player::PT_LOCAL1) || (p->type() == Player::PT_LOCAL2)) {
            addGameStateChange(COMMAND_PLAYERCONTROL " %i %i %i", (int)p->heading, (int)p->moving, (int)p->bombing);
        }//if
    }//for
    return clientConnection.WriteData(gamestatepacket.c_str());
}


bool Game::recvGameState()
{
    CommandStruct cmd;        // receive server data
    Position pos;
    if (clientConnection.ReadData()) {
	    while (clientConnection.readCommandFromBuffer(cmd)) {

            if (cmd.cmd == COMMAND_BOMB) {  //BOMB PLACING
                pos = Position(cmd.intparams[1], cmd.intparams[2]);
                if (bombAtPosition(pos) == bombs.end()) {
    		        bombs.push_back(Bomb(cmd.intparams[0], pos, globals.getGameTimer(), cmd.intparams[3]));
                }//if
            }//if
/*            else if (cmd.cmd == COMMAND_EXPLODE) {  //BOMB EXPLOSION
		        Bombs::iterator b = bombAtPosition(Position(cmd.intparams[0],cmd.intparams[1]));
		        if (b != bombs.end()) {  //TODO: ignore or test in xbombs list
		            bombExplosion(*b);
                    xbombs.push_back(*b);
                    bombs.erase(b);
                }//if
		    }//if*/
		    
		    else if (cmd.cmd == COMMAND_PLAYERPOSITION) {  //PLAYER'S position
                Player &p = findByPID(cmd.intparams[0]);
                if (p.pid == 0) {
                    logger->log("received data for unknown player");
                }//if
                p.px = float(cmd.intparams[1]) / STEP_PRECISION;
                p.py = float(cmd.intparams[2]) / STEP_PRECISION;
                p.heading = (Direction)cmd.intparams[3];
                p.moving = (cmd.intparams[4] != 0);
		    }//if
            else if (cmd.cmd == COMMAND_GAMEOVER) {
                return false;
            }//if
		    else if (cmd.cmd == COMMAND_DEATH) {  // PLAYER'S DEATH
                Player &p = findByPID(cmd.intparams[0]);
                p.alive = false;
            }//if
            else if (cmd.cmd == COMMAND_SCORE) {
                Player &p = findByPID(cmd.intparams[0]);
                p.score = cmd.intparams[1];
            }//if
            else if (cmd.cmd == COMMAND_TIMEOUT) { //send with init data
                timelimit = cmd.intparams[0];
            }//if
            else if (cmd.cmd == COMMAND_EXIT) {
                gltMessageBox("Error:","Server shutdown.");
                return false;
            }//if
            else 
                logger->log("Unknown message from server: ", cmd.cmd);
		}//while
        
    }//if
    else {
        //TODO:connection failed - reconnect
    }//else
    return true;
}

bool Game::sendInitData() 
{
    clearGameStateChange();

    addGameStateChange(COMMAND_GAME  " %s %i %i ", 
                       exportBoard().c_str(), 
                       int(gwidth), int(gheight));
    addGameStateChange(COMMAND_TIMEOUT " %i", (int)GAMETIMELIMIT);
    timelimit = GAMETIMELIMIT;

    for (Players::iterator p = players.begin(); p != players.end(); ++p) {
        addGameStateChange(COMMAND_PLAYERPOSITION " %i %i %i %i %i", 
                         int(p->pid), 
                         int(p->px*STEP_PRECISION), 
                         int(p->py*STEP_PRECISION), 
                         (int)p->heading, 
                         (int)p->moving);
    }//for
    broadcastGameStateChange();
    return true;    
}

bool Game::updateGameState(bool sendPlayerPos)
{

    // CHANGE POSITION OF MOVING PLAYERS
    // AND POWERUP-PICKUP TEST
	for (Players::iterator p = players.begin(); p != players.end(); ++p) {
		if ((p->alive) && (p->moving)) {
		    //float x0 = p->px; // obsolete - on players control-change we send all players positions
		    //float y0 = p->py;
		    //Direction h0 = p->heading;
		    if (glocal) { movePlayer(*p); }
		    for (PowerUps::iterator pi = powerups.begin(); pi != powerups.end(); ++pi) {
		        if (pi->pos == p->cellpos()) {
		            p->pickupPowerUp(*pi);
		            addGameStateChange(COMMAND_POWERUP " %i %i %i", (int)p->pid, (int)pi->type, (int)pi->data);
		            powerups.erase(pi);
		            break;
		        }//if
		    }//for
		}//if moving
		if (sendPlayerPos || p->moving) {
    	    addGameStateChange(COMMAND_PLAYERPOSITION " %i %i %i %i %i", int(p->pid), int(p->px*STEP_PRECISION), int(p->py*STEP_PRECISION), (int)p->heading, (int)p->moving);
		}//if
		 // only server places bombs
		if ((glocal) && (p->alive) && (p->bombing) && (cell(p->cellpos()) == CELL_EMPTY)) {
		    if (playersBombs(p->pid) < p->getMaxBombs() ) {
    		    bombs.push_back(Bomb(p->pid, p->cellpos(), globals.getGameTimer(), BOMBSTRENGTH+p->bonusstrength));
    	        addGameStateChange(COMMAND_BOMB " %i %i %i %i", (int)p->pid, (int)((p->cellpos()).x), (int)((p->cellpos()).y), (int)(BOMBSTRENGTH+p->bonusstrength));
		    }//if
		}//if bombing
	}//for players

    //EXPLODING BOMBS
    for (Bombs::iterator xb = xbombs.begin(); xb != xbombs.end(); ) {
        xb->data[0]++;
        if (xb->data[0] >= XTIMER) {
		    xb = xbombs.erase(xb);
	    } else {
		    ++xb;
	    }//if/else
    }//for	    
    
    //BOMBS
    for (Bombs::iterator b = bombs.begin(); b != bombs.end(); ) {
        if ((b->time + BOMBTIMEOUT) <= globals.getGameTimer() ) {
            bombExplosion(*b);
            xbombs.push_back(*b);
            b = bombs.erase(b);
        } else {
            ++b;
        }//if/else
    }//for bombs

    //GAMEOVER TEST
    if (glocal) {
        int timeout = timelimit - (globals.getGameTimer() - gamestart);
        if (timeout <= 0) {
            addGameStateChange(COMMAND_GAMEOVER " timeout");
            return false;
        }//if
        if ((alivePlayers() <= 1) && bombs.empty() && xbombs.empty()) {
            addGameStateChange(COMMAND_GAMEOVER " bombed!");
            return false;
        }//if
    }//if
    return true;
}

