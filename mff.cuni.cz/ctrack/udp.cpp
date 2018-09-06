#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <time.h>

#include "error.h"
#include "config.h"
#include "udp.h"
#include "str.h"

typedef enum { PACKET_CONNECT=0, PACKET_ANNOUNCE=1, PACKET_SCRAPE=2, PACKET_ERROR=3, PACKET_UNKNOWN=100 } PACKET_TYPE;

static PACKET_TYPE GetPacketType(UDPPacket *inbuffer);
static int FillAnnounceNodes(Peers *peers, PPeerInfo client, EndPoint *node, int numwant);

#define MAX_ANNOUNCE_NODES ((int)((UDP_BUFFER_SIZE-sizeof(AnnounceOutput))/sizeof(EndPoint)))

static INT64 conn_id = 0x1C78AC3;
static char INVALID_PACKET[] = "Invalid packet";
static char INVALID_SCRAPE[] = "Invalid scrape packet";
static char NO_TORRENT[] = "Unknown torrent";

ssize_t UDPMain(const void *inbuffer, size_t size_in, void *outbuffer, struct sockaddr_in *sa)
{
    UDPPacket in, out;
    PTorrentInfo ti;
    PPeerInfo peer;
    in.buffer = inbuffer;
    out.buffer = outbuffer;

    int num;
    PACKET_TYPE ptype = GetPacketType(&in);

    out.conn_out->transaction_id = in.conn_in->transaction_id;
    out.conn_out->action = in.conn_in->action;
    logf("udp: action: %i (type: %i); ", (int)ntohl(in.announce_in->action), ptype);
    
    switch (ptype) {

        case PACKET_CONNECT:   // CONNECT
            out.conn_out->connection_id = conn_id;
            return sizeof(ConnectOutput);

        case PACKET_ANNOUNCE:  // ANNOUNCE
            char b[41];
            hashtostr(in.announce_in->info_hash, b);
            logf("udp: announce (%s): %x:%i;", b, (int)in.announce_in->address.addr, (int)ntohs(in.announce_in->port));
            if (TorrentDBGet(in.announce_in->info_hash, &ti, TRUE) == FALSE) {
                out.error_out->action = htonl(3);
                strcpy(&(out.error_out->message), NO_TORRENT);
                return (sizeof(ErrorOutput) + strlen(NO_TORRENT));
            } else {
                if (FindPeer(ti, in.announce_in->peer_id, &peer) == FALSE) { 
                	UpdatePeerData(ti); // new peer
                }
                if (ntohl(in.announce_in->event) == 1) { 
                	ti->downloaded++; // new completed download
                	UpdatePeerData(ti);
                }//if
                if (in.announce_in->address.addr == 0) {
                	peer->ip.inaddr = sa->sin_addr;
                } else {
                	peer->ip = in.announce_in->address;
                }
                peer->port = ntohs(in.announce_in->port);
                peer->bytesleft = ntoh64(in.announce_in->left);
                peer->last_announce = time(NULL);
                out.announce_out->interval = htonl(*announce_int);
                out.announce_out->leechers = htonl(ti->leech_count);
                out.announce_out->seeders = htonl(ti->seed_count);

                num = ntohl(in.announce_in->numwant);
                if (num == -1) num = ti->peers->size();
                if (num > MAX_ANNOUNCE_NODES) num = MAX_ANNOUNCE_NODES;
                num = FillAnnounceNodes(ti->peers, peer, out.announce_out->peers, num);

                return (sizeof(AnnounceOutput) + sizeof(EndPoint)*(num-1));
            }//else

        case PACKET_SCRAPE: // SCRAPE 
            //num = ntohs(in.scrape_in->count); -- incorect spec
            num = (int)((size_in - sizeof(ScrapeInput)) / 20) + 1;
            if (num > 0) {
	            for (int i = 0; i < num; i++) {
	            	if (TorrentDBGet(&(in.scrape_in->infohashes[20*i]), &ti, FALSE) == FALSE) {
		            	memset(&(out.scrape_out->data[i]), 0, sizeof(ScrapeData));
		            } else {
		            	out.scrape_out->data[i].complete = htonl(ti->downloaded);
		            	out.scrape_out->data[i].seeds =    htonl(ti->seed_count);
		            	out.scrape_out->data[i].leechers = htonl(ti->leech_count);
		            }
	            }//for
	            return (sizeof(ScrapeOutput) + sizeof(ScrapeData)*(num-1));
			} else {
	            out.error_out->action = htonl(3);
    	        strcpy(&(out.error_out->message), INVALID_SCRAPE);
           		log("Invalid UDP scrape packet");            
        	    return (sizeof(ErrorOutput) + strlen(INVALID_SCRAPE));
            }
        default:
            out.error_out->action = htonl(3);
            strcpy(&(out.error_out->message), INVALID_PACKET);
            log("Unknown UDP packet");            
            return (sizeof(ErrorOutput) + strlen(INVALID_PACKET));
    }//switch

}

static int FillAnnounceNodes(Peers *peers, PPeerInfo client, EndPoint *node, int numwant)
{
    int count = 0;
    Peers::iterator it = peers->begin();
    while (it != peers->end()) {
        PPeerInfo peer = *it;
        if (peer != client) {
            node[count].address = peer->ip;
            node[count].port = htons(peer->port);
            count++;
            if (count >= numwant) break;
        }//if
        ++it;
    }//for
    const int RCOEF = (int)(RAND_MAX*numwant/peers->size());
    while (it != peers->end()) {
        PPeerInfo peer = *it;
        int pos = rand() % count;
        if (rand() > RCOEF) {
            node[pos].address = peer->ip;
            node[pos].port = htons(peer->port);
        }//if
        ++it;
    }
    return count;
}

static const char CONN_PACKET_ID[8] = 
    { 0x00, 0x00, 0x04, 0x17, 0x27, 0x10, 0x19, 0x80 };

static PACKET_TYPE GetPacketType(UDPPacket *packet)
{

    if ((packet->conn_in->action == 0) && (memcmp(&(packet->conn_in->connection_id), CONN_PACKET_ID, 8) == 0)) 
        return PACKET_CONNECT;
    if (ntohl(packet->announce_in->action) == 1) return PACKET_ANNOUNCE;
    if (ntohl(packet->announce_in->action) == 2) return PACKET_SCRAPE;
    return PACKET_UNKNOWN;
}
