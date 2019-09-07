#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <string.h>

#include "error.h"
#include "server.h"
#include "config.h"
#include "threads.h"
#include "udp.h"
#include "db.h"
#include "str.h"

static SOCKET ssd = INVALID_SOCKET; // HTTP socket
static SOCKET udp_sd = INVALID_SOCKET; // udp socket

int SetUpListener()
{
    unsigned int port;
    SOCKET sd;
    struct sockaddr_in sinInterface;

    port = GetConfigUInt(CFG_HTTP_PORT);
    if (port == 0) {
        port = GetConfigUInt(CFG_SERVER_PORT);
    }//if

    if (port == 0) {
        errorm("HTTP port not specified");
        return FALSE;
    }//if

    logf("Creating TCP server socket (port: %u).", port);

    //struct protoent *pp;
    //getprotobyname("tcp");
    sd = socket(AF_INET, SOCK_STREAM, 0);
    if (sd == INVALID_SOCKET) { 
        errorm("socket() for tcp failed: %s", str_error());   
        return FALSE;
    }
    // SO_REUSEADDR
    int one = 1;
    if (setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(int)) != 0) {
        errorm("setsockopt(SO_REUSEADDR) for tcp failed: %s", str_error());
      }

    sinInterface.sin_family = AF_INET;
    sinInterface.sin_addr.s_addr = INADDR_ANY;
    sinInterface.sin_port = htons((u_short)port);
    if (bind(sd, (struct sockaddr *)&sinInterface, sizeof(sinInterface)) == INVALID_SOCKET) { 
        errorm("bind() for tcp failed: %s", str_error()); 
        return FALSE;
    }

    if (listen(sd, SOMAXCONN) == SOCKET_ERROR) { 
        errorm("listen() for tcp failed: %s", str_error()); 
        return FALSE;
    }

    ssd = sd;
   
    return TRUE;
}

void CloseTCPSocket()
{
    if (ssd != INVALID_SOCKET) {
        log("Closing HTTP server socket...");
        close(ssd);
        ssd = INVALID_SOCKET;
    } else {
        errorm("Cannot close HTTP server socket (invalid descriptor).");
    }
}

extern int ThreadInitCode();

void *HTTPServerMain(void *)
{
    struct ClientConnData ccdata;
    SOCKET newsock;
    struct sockaddr_in cs;
    size_t css = sizeof(cs);

	ThreadInitCode();

    while (c_control == C_RUN) {
        newsock = accept(ssd, (struct sockaddr *)&cs, (socklen_t *)&css);

		if (c_control != C_RUN) { break; } //immediate exit - don't print error

        if (newsock != -1) {

            ccdata.action = ACTION_ACCEPT;
            ccdata.sd = newsock;
            ccdata.port = ntohs(cs.sin_port);
            ccdata.address.inaddr = cs.sin_addr;
            //memcpy(&(ccdata.address), &(cs.sin_addr), sizeof(ccdata.address));

            logf("Accepted connection from %s:%u, socket %u",
                inet_ntoa(ccdata.address.inaddr), 
                ccdata.port, 
                ccdata.sd);

            WakeUpWorkerThread(&ccdata);

        } else {
           errorm("Accept() failed: %s", str_error());
        }//else

    }//while
	return NULL;
}

//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////
//                    UDP 
//////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////

void *UDPServer(void *)
{
    
    unsigned int port;
    void *inbuffer;
    void *outbuffer;

	ThreadInitCode();

/*    if (status_ptr == NULL) { // no parameter is passed
        errorm("UDP thread started with NULL parameter");
        return NULL;
    }//if*/

    port = GetConfigUInt(CFG_UDP_PORT);
    if (port == 0) {
        port = GetConfigUInt(CFG_SERVER_PORT);
    }//if

    if (port == 0) {
        errorm("UDP port not specified");
        return NULL;
    }//if

    logf("Creating server socket (port: %u).", port);

    struct protoent *pp;
    pp = getprotobyname("udp");
    int protonum = 0;
    if (pp != NULL) { protonum = pp->p_proto; }

    udp_sd = socket(AF_INET, SOCK_DGRAM, protonum);
    if (udp_sd == -1) { 
        errorm("socket() failed: %s", str_error());
        return NULL;  
    }//if

    struct sockaddr_in sinInterface;
    sinInterface.sin_family = AF_INET;
    sinInterface.sin_addr.s_addr = INADDR_ANY;
    sinInterface.sin_port = htons(port);
    if (bind(udp_sd, (struct sockaddr *)&sinInterface, sizeof(sinInterface)) == -1) { 
        errorm("bind() failed for udp server: %s", str_error());  
    }//if

    logf("UDP server started...");

    inbuffer = emalloc(UDP_BUFFER_SIZE);
    outbuffer = emalloc(UDP_BUFFER_SIZE);
    
    while (c_control == C_RUN) {
    
        struct sockaddr_in sa;
        socklen_t sl;
        ssize_t inmsgsize;
        ssize_t outmsgsize;
		char *pbuffer;
		sl = sizeof(sa);

        inmsgsize = recvfrom(udp_sd, inbuffer, UDP_BUFFER_SIZE, 0, (struct sockaddr*)&sa, &sl);

		if (c_control != C_RUN) { break; } //immediate exit - don't print error
		
		if (inmsgsize == -1) {
			errorm("recvfrom() failed: %s", str_error());
		} else {
	        pbuffer = hexdump((char*)inbuffer, inmsgsize);
    	    logf("in: \n%s", pbuffer);
			free(pbuffer);

			DBLock();
	        outmsgsize = UDPMain(inbuffer, inmsgsize, outbuffer, &sa);
	        DBUnlock();

	        pbuffer = hexdump((char*)outbuffer, outmsgsize);
	        logf("out: \n%s", pbuffer);
			free(pbuffer);

	        ssize_t sent = sendto(udp_sd, outbuffer, outmsgsize, 0, (struct sockaddr*)&sa, sl);
	        logf("udp in: %i, out: %i (sent: %i)", inmsgsize, outmsgsize, (int)sent);

	        if (sent == -1) { errorm("sendto() failed: %s",str_error()); }
		}//else

    }//while

    return NULL;

}

void CloseUDPSocket()
{
    if (udp_sd != INVALID_SOCKET) {
        log("Closing UDP server socket.");
        close(udp_sd);
        udp_sd = INVALID_SOCKET;
    }//if
}

//////////////////////////////////////////////////////////////////////////////
/////                SUPPORT
//////////////////////////////////////////////////////////////////////////////

/* Converts ascii text to in_addr struct.  
  NULL is returned if the address can not be found. */
int atoaddr(const char *address, IPAddress *result) {
    struct hostent *host;

// SunOS
//   if (inet_pton(AF_INET, pval, &inaddr)) {

/*  LINUX
    if (inet_aton(address, &(result->inaddr))) {
        return TRUE;
    }*/

    host = gethostbyname(address);
    if (host != NULL) { 
        memcpy(&(result->inaddr), host->h_addr_list, 4); 
        return TRUE;
    }
    return FALSE;
}

