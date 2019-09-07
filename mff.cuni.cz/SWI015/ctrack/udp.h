#ifndef udp_h
#define udp_h

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "db.h"
#include "error.h"

typedef struct {
	INT64 connection_id; // 0x00 0x00 0x04 0x17 0x27 0x10 0x19 0x80
	INT32 action; // 0
	INT32 transaction_id;
} ConnectInput, *PConnectInput;

typedef struct {
	INT32 action; // 0
	INT32 transaction_id;
	INT64 connection_id;
} ConnectOutput, *PConnectOutput;

typedef struct  {
	INT64  connection_id;
	INT32  action;		// 1
	INT32  transaction_id;
	char   info_hash[20];
	char   peer_id[20];
	INT64  downloaded;
	INT64  left;
	INT64  uploaded;
	INT32  event;
	IPAddress address;
	INT32  key;
	INT32  numwant;
	UINT32 port;
	UINT16 extensions;
} AnnounceInput, *PAnnounceInput;

typedef struct  {
	IPAddress address;
	UINT16 port;
} EndPoint;

typedef struct  {
	INT32 action; // 1
	INT32 transaction_id;
	INT32 interval;
	INT32 leechers;
	INT32 seeders;
	EndPoint peers[1];
} AnnounceOutput,*PAnnounceOutput;

typedef struct  {
	INT64    connection_id;
	INT32	 action;		// 2
	INT32	 transaction_id;
	//INT16    count;  // number of infohashes -- only in some specs / azureus doesn't use
	UINT16   extensions;
	char     infohashes[20]; // list of info hashes
} ScrapeInput,*PScrapeInput;

typedef struct {
    INT32   seeds;   // order of members differs in various specs !
    INT32   complete; // number of completed downloads
    INT32   leechers; 
} ScrapeData;

typedef struct  {
	INT32	action;		// 2
	INT32	transaction_id;
	ScrapeData data[1];
} ScrapeOutput,*PScrapeOutput;

typedef struct {
	INT32 action; // 3
	INT32 transaction_id;
	char message;
} ErrorOutput, *PErrorOutput;

typedef struct {
    union {
        ConnectInput   *conn_in;
        ConnectOutput  *conn_out;
        AnnounceInput  *announce_in;
        AnnounceOutput *announce_out;
        ScrapeInput    *scrape_in;
        ScrapeOutput   *scrape_out;
        ErrorOutput    *error_out;
        const void     *buffer;
    };
    //size_t  size; 
} UDPPacket;

#define UDP_BUFFER_SIZE (4096 * sizeof(char))    // UDP buffer

extern ssize_t UDPMain(const void *inbuffer, size_t size_in, 
                     void *outbuffer, struct sockaddr_in *sa);
#endif
