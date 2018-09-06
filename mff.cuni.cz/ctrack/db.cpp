#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>
#include <time.h>
#include <list>

#include "db.h"
#include "error.h"
#include "str.h"
#include "config.h"

/** 
 database of torrents & asociated clients 
 access requires synchronization
*/

using namespace std;

// DATA
typedef list<PTorrentInfo> Torrents;

static Torrents torr_db;

static pthread_mutex_t db_mutex = 
        PTHREAD_MUTEX_INITIALIZER; // db file access mutex

// CODE

void DBLock() {
    pthread_mutex_lock(&db_mutex);	
}
void DBUnlock() {
    pthread_mutex_unlock(&db_mutex);	
}

int TorrentDBCreate()
{
   // nothing, for now
   return TRUE;
}

int TorrentDBGet(InfoHash hash, PTorrentInfo *result, int can_add)
{
    PTorrentInfo t;
    for (Torrents::iterator i = torr_db.begin(); i != torr_db.end(); ++i) {
	    t = *i;
        if (memcmp(t->info_hash, hash, 20) == 0) {
            *result = t;
            return TRUE;
        }//if
    }//for
    if (can_add && (GetConfigBool(CFG_OPEN_DB) != FALSE)) {
    	NewTorrentInfo(&t, hash);
    	torr_db.push_back(t);
        *result = t;
        return TRUE;
    }//if
    return FALSE;
}

int NewTorrentInfo(PTorrentInfo *t, InfoHash info_hash)
{
	PTorrentInfo torr = new TorrentInfo;
	memset(torr, 0, sizeof(TorrentInfo));
   	memcpy(torr->info_hash, info_hash, 20);
   	torr->peers = new Peers;
   	*t = torr;
	return TRUE;
}

int TorrentDBInsert(PTorrentInfo t)
{
    torr_db.push_back(t);
    return TRUE;
}


int FindPeer(PTorrentInfo torrent, PeerID peer, PPeerInfo *result)
{
    PPeerInfo pi;
    for (Peers::iterator it = torrent->peers->begin();  it != torrent->peers->end(); ++it) {
        pi = *it;
        if (memcmp(peer, pi->peer_id, 20) == 0) {
            pi->last_announce = time(NULL);
            *result = pi;
            return TRUE;
        }
    }//for
    pi = new PeerInfo;
    memset(pi, 0, sizeof(PeerInfo));
    memcpy(pi->peer_id, peer, 20);
    pi->last_announce = time(NULL);
    torrent->peers->push_back(pi);
    *result = pi;
    return FALSE;
}


int UpdatePeerData(PTorrentInfo torrent)
{
    PPeerInfo pi;
	Peers *p = torrent->peers;
	time_t curr = time(NULL);
	torrent->seed_count = 0;
	torrent->leech_count = 0;
    Peers::iterator it =  p->begin();
    while (it != p->end()) {
        pi = *it;
        if ((time_t)(pi->last_announce + INACTIVE_TIMEOUT) < curr) {
        	it = p->erase(it);
        } else {
	        if (pi->bytesleft == 0) { torrent->seed_count++; }
        	 else { torrent->leech_count++; }
	        ++it;
        }
    }//for
	return TRUE;
}

