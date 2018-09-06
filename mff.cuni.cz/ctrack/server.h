#ifndef server_h
#define server_h

#include "error.h"
#include "db.h"

#define ACTION_ACCEPT (0x0AA0)
//#define ACTION_EXIT (0x0AE0)

//typedef 
struct ClientConnData {
	int action;
	SOCKET sd;
	int	port;
	IPAddress address;
};

extern SOCKET SetUpListener();

extern void CloseTCPSocket();

extern void *HTTPServerMain(void *);


extern void *UDPServer(void *status_ptr);

extern void CloseUDPSocket();

/* Converts ascii text to in_addr struct (IPAddress).  
  FALSE is returned if the address can not be found. */
extern int atoaddr(const char *address, IPAddress *result);

#endif
