#include "ai.h"

#include <string>
#include <deque>
#include <fstream>
#include "logger.h"

using namespace std;

typedef deque <char*> Strings;
Strings aiNames;  // names of AI  players

extern bool aiPlay(Game&, Player&);

static int* buffer;
static int* buffer2;
static int dummy;

static int boardwidth;
static int boardheight;
static int buffersize;

extern void clearBuffers(Game&); // inits and clears buffers
//extern void clearBuffer(Game&); 
//extern void clearBuffer2(Game&); 
extern int& buffercell(int x, int y);
extern int& buffercell(Position p);

int& buffercell(Position p) {
    return buffercell(p.x,p.y);
}
int& buffercell(int x, int y) {
    if ((x >=0) && (x < boardheight) && (y>=0) && (y < boardwidth)) {
        return buffer[x + (y * boardwidth)];
    } else {
        return dummy;
    }
}

bool aiInit()
{
    buffersize = 0;
    buffer = NULL;
    buffer2 = NULL;
    
	ifstream namelist;
	namelist.open("data/names.txt", ios::in);
    if (namelist.is_open()) {  
	    string buffer;
	    while (!namelist.eof()) {
	        getline(namelist, buffer);
            if (!buffer.empty()) {
                char *name = new char[buffer.length()+1];
                strcpy(name, buffer.c_str());
                aiNames.push_back(name);
            }//if
	    }//while
    }//if
    namelist.close();
    return true; 
}

static char defaultName[] = "[bot]computer";

const char* aiPlayerName(Game& game) 
{
    for (Strings::iterator n = aiNames.begin(); n != aiNames.end(); ++n) {
        bool used = false;
        for (Players::iterator p = game.players.begin(); p != game.players.end(); ++p) {
            if (p->name == *n) { 
                used = true;
            }//if
        }//for
        if (!used) {
            return *n;
        }//if
    }//for
    return defaultName;
}

bool aiControl(Game& game)
{
    for (Players::iterator pi = game.players.begin(); pi != game.players.end(); ++pi) {
        if (pi->type() == Player::PT_AI) {
            if (!aiPlay(game, *pi)) {
                logger->log("AI failed", pi->name);
            }//if;
            //TODO: do something

        }//if
    }//for
    return true;
}

void clearBuffers(Game& game) 
{
    boardheight = game.getHeight();
    boardwidth = game.getWidth();
    int sizereq = boardwidth*boardheight + 1;
    if (buffersize < sizereq || (buffer=NULL) || (buffer2==NULL)) {
        buffersize = sizereq;
        if (buffer != NULL) { delete[] buffer; }
        if (buffer2 != NULL) { delete[] buffer2; }
        buffer = new int[buffersize];
        buffer2 = new int[buffersize];
        memset(buffer, 0, buffersize*sizeof(int));
        memset(buffer2, 0, buffersize*sizeof(int));
    }//if
}
bool aiWave(Game& game, Position p) 
{
    memset(buffer, 1024, buffersize*sizeof(int));
    
    bool changed = false;
    buffercell(-1,-1) = 1024;
    for (int i = 1; i < 10; i++){
        for (int y = 0; y < boardheight; y++)  {
            for (int x = 0; y < boardwidth; x++) {
                int cell = buffercell(x,y);
                cell = min(cell, buffercell(x+1,y));
                cell = min(cell, buffercell(x-1,y));
                cell = min(cell, buffercell(x,y+1));
                cell = min(cell, buffercell(x,y-1));
            }//for
        }//for
    }//for
    return true;
}

bool aiPlay(Game& game, Player& p)
{
    clearBuffers(game);
    aiWave(game, p.cellpos());
    
    for (Players::iterator pi = game.players.begin(); pi != game.players.end(); ++pi) {
        if (pi->pid != p.pid) {
        //TODO: check player
        }//if
    }//for
//    nearestEnemy();
    return true;
}

