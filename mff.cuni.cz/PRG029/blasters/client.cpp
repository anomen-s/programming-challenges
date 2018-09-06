#include "net.h"


std::string& GetServerIncomingBuffer()
{
    return clientConnection.acBuffer;
}

bool ConnectToServer(const char *server, unsigned short port)
{
	SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (sock == INVALID_SOCKET) { FAILURE(sock, "socket"); }

	sockaddr_in addr; // for connecting to the server
	addr.sin_family = AF_INET;  // An Internet Socket
	addr.sin_port = htons(port);  // port must be in network order

	hostent *r_host;
    if(inet_addr(server)==INADDR_NONE)   // Resolve by hostname
    {
        r_host=gethostbyname(server);
    }
    else {
        unsigned long addr = inet_addr(server);
        r_host=gethostbyaddr((char*)&addr, sizeof(addr), AF_INET);
    }
	if (r_host == NULL) { FAILURE(sock, "gethostbyname"); }

	memcpy(&addr.sin_addr.s_addr, r_host->h_addr, r_host->h_length);

	u_long nonblock = 1;
	if (ioctlsocket(sock, FIONBIO, &nonblock) == SOCKET_ERROR) { FAILURE(sock, "ioctlsocket"); }


	clientConnection.sd = sock;

    if (connect(sock,(struct sockaddr *)&addr,sizeof(addr)) == SOCKET_ERROR) {
        //  WSAEWOULDBLOCK
        if (SaveLastWinsockError("connect") != WSAEWOULDBLOCK) {
            return false;
        }//if
    }//if

    // WAIT FOR CONNECTION ...
    timeval t;
    t.tv_sec = 1;
    t.tv_usec = 0;
    fd_set WriteFDs, ExceptFDs;

    for (int i = 5; i > 0; i--) {

        extern bool DrawGetStr(const char* prompt, const char* text);
        DrawGetStr("Connecting...", strprintf("Time: %i", i).c_str());
        SwapBuffers(globals.hDC);

        FD_ZERO(&WriteFDs); FD_SET(sock, &WriteFDs);
        FD_ZERO(&ExceptFDs);FD_SET(sock, &ExceptFDs);

        switch (select(0, NULL, &WriteFDs, &ExceptFDs, &t)) {
        case SOCKET_ERROR: // error
            SaveLastWinsockError("select");
            return true;
        case 0:     // timeout
            break;
        case 1:     // something has happened
            if (FD_ISSET(sock, &WriteFDs)) {
                return true;
            }//if
            if (FD_ISSET(sock, &ExceptFDs)) {
                return false;
            }//if
            break;
        default:
            break;// ????
        }//switch:
    }//for
	
    return true; //select returned nothing, but hope still lives :-)
}
