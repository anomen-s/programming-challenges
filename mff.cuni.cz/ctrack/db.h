#ifndef db_h
#define db_h

#include <vector>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "error.h"

#define INACTIVE_TIMEOUT ((time_t)(*announce_int))  // period for removing inactive nodes

typedef const char* InfoHash;
typedef const char* PeerID;

typedef struct  {
    union {
	   unsigned char    bytes[4];
	   UINT32  addr;
	   struct in_addr inaddr;
	};
} IPAddress;

typedef struct {
    char peer_id[20];
    IPAddress ip;
    unsigned int port;
    INT64 bytesleft;  
    time_t last_announce;
} PeerInfo, *PPeerInfo;

typedef std::vector<PPeerInfo> Peers;

typedef struct {
    char    info_hash[20]; // info hash
    char   	*name;       // name (optional)
    char 	*key;
    INT32	udp_key;
    int     downloaded; // number of complete downloads
    Peers  	*peers;      // list of clients
    int     seed_count; // number of seeds
    int     leech_count; // number of peers
//    int     dbpos;     // position in db
//    int     dbsize;      // size in db
} TorrentInfo;

typedef TorrentInfo *PTorrentInfo;


// lock db
void DBLock();
// unlocks db
void DBUnlock();

// creates torrent db
extern int TorrentDBCreate();

/* looks for TorrentInfo structure for given hash
 TODO: if config(opendb) then create
*/
extern int TorrentDBGet(InfoHash hash, PTorrentInfo *result, int can_add);

// inserts new TorrentInfo structure
extern int TorrentDBInsert(PTorrentInfo t);

// creates new empty TorrentInfo
extern int NewTorrentInfo(PTorrentInfo *t, InfoHash info_hash);

// finds peer with given id for given torrent
// returns FALSE if new peer
extern int FindPeer(PTorrentInfo torrent, PeerID peer, PPeerInfo *result);

// actualizes peer data (seed/leech count, drops dead peers 
extern int UpdatePeerData(PTorrentInfo torrent);

#endif

