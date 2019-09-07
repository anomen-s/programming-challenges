#ifndef http_h
#define http_h

#include "server.h"
#include "error.h"
#include "db.h"

#define METHOD_ANNOUNCE (0xDA)
#define METHOD_SCRAPE (0xDC)
#define METHOD_INVALID (0x00)

typedef struct{
	char		info_hash[20];
	char		peer_id[20];
	INT64 		left;
	UINT16 		port;
	IPAddress	address;
	const char *key;
	int	  		numwant;
	int 		event;
	int         method;
} HTTP_REQUEST, *PHTTP_REQUEST;

extern int HTTPMain(struct ClientConnData *ccdata);

#endif

