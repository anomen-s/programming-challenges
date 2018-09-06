#ifndef net_h
#define net_h

#include <winsock.h>
#include <string>
#include <deque>

#include "gamedata.h"

//#define UM_SOCKRECV (WM_USER+22) // callback message for socket events /abandoned/

#define COMMAND_ACCEPT "ACCEPT"  // S: handshake (pid)
#define COMMAND_REJECT "REJECT"  // S: handshake ({reason})
#define COMMAND_HELLO "HELLO"    // C: handshake (name)

#define COMMAND_GAME "GAME"      // S: handshake ([data....],width,height)
#define COMMAND_PLAYERLIST "PLYRS"  // S: new player list (clear current)
#define COMMAND_PLAYER "PLYR"  // S: player ({name}, pid, score)

#define COMMAND_PLAYERCONTROL "CTRL"    // C: player controls (heading,moving,bombing)
#define COMMAND_EXPLODE "EXPL"          // S: BOMB EXPLOSION (x,y)
#define COMMAND_POWERUPDESTROY "PUPX"   //?S: powerup destroyed by bomb (x,y)
#define COMMAND_BOMB "BOMB"             // S: new bomb (pid,x,y,strength)
#define COMMAND_POWERUP "PWUP"          // S: picked up powerup (pid,type,data)
#define COMMAND_PLAYERPOSITION "PPOS"   // S: player position (pid,x,y,heading,moving)
#define COMMAND_GAMEOVER "GMOVR"        // S: game over
#define COMMAND_DEATH "DEAD"            // S: player dead (pid)
#define COMMAND_TIMEOUT "TIME"          //?S: player dead (time [ms])
#define COMMAND_SCORE "SCORE"           // S: player's score (pid,score)

#define COMMAND_PING "PING"             // S/C: ping ({str_arg})
#define COMMAND_PONG "PONG"             // S/C: ping reply ({str_arg})

#define COMMAND_EXIT "EXIT"             // S/C: exit {reason}


// parsed command
struct CommandStruct {
    std::string  cmd;
    std::string  strparam;
    int     intparams[8];
};

struct Connection {
    SOCKET  sd;
    u_long  ip;
    PID     pid; // remote player's ID, 0=handshaking still in progress
    long    ping;
    std::string  acBuffer; // incoming buffer

    Connection() : sd(INVALID_SOCKET), pid(0), ip(0), ping(-1) { }
    Connection(SOCKET sd_, u_long ip_) : sd(sd_), pid(0), ip(ip_), ping(-1) { }
    bool ReadData();
    bool WriteData(const char* buffer);
    void Close();
    bool readCommandFromBuffer(CommandStruct& cmd); // returns true if command read
};

//extern bool ReadData(Connection& conn);      -- moved into Connection object
//extern bool WriteData(Connection& conn, const char* buffer);

// encode/decode string (replace spaces with underscores
extern std::string encode(std::string);
extern std::string decode(std::string);


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
/// CLIENT
////////////////////////////////////////////////////////////
extern Connection clientConnection;

extern bool ConnectToServer(const char *server, unsigned short port);
extern std::string& GetServerIncomingBuffer();


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
/// SERVER
////////////////////////////////////////////////////////////

typedef std::deque<Connection> Connections;
extern Connections gConnections;

extern SOCKET gameserversock;

extern bool SetUpListener(unsigned short nPort);

// AcceptConnections
// accepts incoming  connections AND read incoming data from clients
// returns true if new connection was estabilished
extern bool AcceptConnections();

// returns true if there are still more connections waiting for handshake
extern bool AcceptNewPlayer(PID pid);

// sends data to all active clients
extern bool SendToClients(const char* buffer);

// kicks all clients with zero PID
extern void KickUnacceptedClients(const char* reason);

// returns incoming buffer for given player
//extern std::string& GetClientIncomingBuffer(PID player);

// reads first command in buffer of specified player
extern bool readCommandFromPlayer(PID, CommandStruct& cmd);

////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
/// WinSock code
////////////////////////////////////////////////////////////

extern bool InitWinSock(void);
extern void CleanupWinSock(void);

extern const char* LastWinSockError(void); //returns error message
extern const char* LastWinSockErrorMessage(void); // returns name of function that caused error and error message

extern bool CloseSocket(SOCKET);
extern int  SaveLastWinsockError(const char* reason, int nErrorID = 0);

//closes server/client connections
extern void CloseGameConnections(void);

// Winsock 2 header defines this, but Winsock 1.1 header doesn't.  In
// the interest of not requiring the Winsock 2 SDK which we don't really
// need, we'll just define this one constant ourselves.
#ifndef SD_SEND
#define SD_SEND 1
#endif

// error macro for inet functions

#define FAILURE(s, func) \
				SaveLastWinsockError(func);   \
   				if ((s) != INVALID_SOCKET) closesocket(s);  \
				return false;


#endif
