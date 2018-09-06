
#include <iostream>

#include "net.h"
#include "globals.h"
#include "logger.h"

using namespace std;


////////////////////////////////////////////////////////////////////////
// Globals and types

Connections gConnections;


  // replaced by readCommandFromPlayer !!!
/*string& GetClientIncomingBuffer(PID player)
{
    static string emptyString = "";
    for (Connections::iterator con = gConnections.begin(); con != gConnections.end(); ++con) {
        if (con->pid == player) {
            return con->acBuffer;
        }//
    }//for
    return emptyString;
}*/

// send data to clients
bool SendToClients(const char* buffer)
{
    bool res = true;
    for (Connections::iterator con = gConnections.begin(); con != gConnections.end(); ++con) {
        if (con->pid >= PID_MIN) {
            res = (con->WriteData(buffer) && res);
        }//if
    }//for
    return res;
}

void KickUnacceptedClients(const char* reason)
{
    Connections::iterator con = gConnections.begin();
    while (con != gConnections.end()) {
        if (con->pid == 0) {
            string rejection = COMMAND_REJECT " ";
            rejection.append(encode(reason)).append(" \r\n");
            con->WriteData(rejection.c_str());
            con->Close();
            con = gConnections.erase(con);
        }//if
        else {
            ++con;
        }
    }//while

}


bool AcceptNewPlayer(PID pid)
{
    bool found = false;
    string packet = strprintf(":Hello, this is Blasters server. Your PID is:\r\n" COMMAND_ACCEPT " %i \r\n", (int)pid);
    Connections::iterator con = gConnections.begin(); 
    while (con != gConnections.end()) {
        if (con->pid == 0) {
            if (con->WriteData(packet.c_str())) {
                con->pid = pid;
                return true;
            }//if
            else { // transfer failed, kill client
                CloseSocket(con->sd);
                con = gConnections.erase(con);
                return true; // thic handshake failed, but there can be more waiting connections
            }//else
        }//if
        ++con;
    }//while
    return false;

}


//// SetUpListener /////////////////////////////////////////////////////
// Sets up a listener on the given interface and port, returning the
// listening socket if successful; if not, returns INVALID_SOCKET.

bool SetUpListener(u_short port)
{
    SOCKET sd = socket(AF_INET, SOCK_STREAM, 0);
    if (sd == INVALID_SOCKET) {	FAILURE(sd, "socket"); 	}

    sockaddr_in sinInterface;
    sinInterface.sin_family = AF_INET;
    sinInterface.sin_addr.s_addr =  htonl(INADDR_ANY);
    sinInterface.sin_port = htons(port);
	if (bind(sd, (LPSOCKADDR)&sinInterface, sizeof(sockaddr_in)) == SOCKET_ERROR) { FAILURE(sd, "bind");	}

    if (listen(sd, SOMAXCONN) == SOCKET_ERROR) { FAILURE(sd, "listen"); }

// TODO: is this required?     
//	u_long NonBlock = 1;
//	if (ioctlsocket(sd, FIONBIO, &NonBlock) == SOCKET_ERROR) { (sd, "ioctlsocket"); }

    CloseGameConnections(); // close previous connections
    gameserversock = sd;
    
/* //TODO: ??
    char infobuffer[10];
    int isize = 10;
    int newsize = 16;
    if (setsockopt(sd, SOL_SOCKET, SO_SNDBUF, (const char*)&newsize, 4) == SOCKET_ERROR) { FAILURE(sd, "setsockopt"); }
    if (getsockopt(sd, SOL_SOCKET, SO_SNDBUF, infobuffer, &isize) == SOCKET_ERROR ) { FAILURE(sd, "getsockopt"); }
*/  
    int newsize = true;
    if (setsockopt(sd, IPPROTO_TCP, TCP_NODELAY, (const char*)&newsize, 4) == SOCKET_ERROR) { FAILURE(sd, "setsockopt"); }
    
    return true;
}



//// SetupFDSets ///////////////////////////////////////////////////////
// Set up the three FD sets used with select() with the sockets in the
// connection list.  Also add one for the listener socket, if we have
// one.

void SetupFDSets(fd_set& ReadFDs, fd_set& WriteFDs, 
        fd_set& ExceptFDs, SOCKET ListeningSocket) 
{
    FD_ZERO(&ReadFDs);
    FD_ZERO(&WriteFDs);
    FD_ZERO(&ExceptFDs);

    // Add the listener socket to the read and except FD sets, if there
    // is one.
    if (ListeningSocket != INVALID_SOCKET) {
        FD_SET(ListeningSocket, &ReadFDs);
        FD_SET(ListeningSocket, &ExceptFDs);
    }

    // Add client connections
    for (Connections::iterator it = gConnections.begin(); it != gConnections.end(); ++it) {
    	FD_SET(it->sd, &ReadFDs);
        FD_SET(it->sd, &WriteFDs);
        FD_SET(it->sd, &ExceptFDs);
    }//for
}



//// AcceptConnections /////////////////////////////////////////////////
// Handle connections.  Return true if new clients were accepted.

bool AcceptConnections()
{
    bool newclients = false;
    sockaddr_in sinRemote;
    int nAddrSize = sizeof(sinRemote);
    timeval t;
    t.tv_sec = 0;
    t.tv_usec = 0;

    fd_set ReadFDs, WriteFDs, ExceptFDs;
    SetupFDSets(ReadFDs, WriteFDs, ExceptFDs, gameserversock);

//    while (
    if (select(0, &ReadFDs, NULL/*&WriteFDs*/, &ExceptFDs, &t) == SOCKET_ERROR) {//> 0) {
        SaveLastWinsockError("select");
        return false;
    }//if
        //// Something happened on one of the sockets.
        // Was it the listener socket?...
        if (FD_ISSET(gameserversock, &ReadFDs)) {
            SOCKET sd = accept(gameserversock, (LPSOCKADDR)&sinRemote, &nAddrSize);
            if (sd != INVALID_SOCKET) {

                int nodelay = true;
                if (setsockopt(sd, IPPROTO_TCP, TCP_NODELAY, (const char*)&nodelay, 4) == SOCKET_ERROR) { FAILURE(sd, "setsockopt"); }
                int isize = 4;
                if (getsockopt(sd, IPPROTO_TCP, TCP_NODELAY, (char*)&nodelay , &isize) == SOCKET_ERROR ) { FAILURE(sd, "getsockopt"); }
                logger->logf("TCP_NODELAY for %i is %i", (int)sd, (int)nodelay);

                // Tell user we accepted the socket, and add it to
                // our connecition list.
                logger->log(strprintf("Accepted connection from %s:%u, socket %u",inet_ntoa(sinRemote.sin_addr), ntohs(sinRemote.sin_port), sd));
                gConnections.push_back(Connection(sd, sinRemote.sin_addr.s_addr));

                newclients = true;
				if ((gConnections.size() + 1) > 64) {
					// For the background on this check, see
					// www.tangentsoft.net/wskfaq/advanced.html#64sockets
					logger->log("WARNING: More than 63 client connections accepted.  This will not work reliably on some Winsock stacks!");
				}//if

                // Mark the socket as non-blocking, for safety.
                u_long nNoBlock = 1;
                ioctlsocket(sd, FIONBIO, &nNoBlock);
            }//if
            else { //sd == INVALID_SOCKET
            	SaveLastWinsockError("accept");
                return false;
            }
        }//if listening
        else if (FD_ISSET(gameserversock, &ExceptFDs)) {
            int err;
            int errlen = sizeof(err);
            getsockopt(gameserversock, SOL_SOCKET, SO_ERROR, (char*)&err, &errlen);
            SaveLastWinsockError("(exceptfds)");
            logger->log("SO_ERROR: ",err);
            return newclients;
        }//if exeptions

        // ...Or was it one of the client sockets?
        Connections::iterator it = gConnections.begin();
        while (it != gConnections.end()) {
            bool bOK = true;
            const char* pcErrorType = NULL;

            // See if this socket's flag is set in any of the FD
            // sets.
            if (FD_ISSET(it->sd, &ExceptFDs)) {
                bOK = false;
                pcErrorType = "General socket error";
                FD_CLR(it->sd, &ExceptFDs);
            }
            else {
                if (FD_ISSET(it->sd, &ReadFDs)) {
                    bOK = it->ReadData();
                    pcErrorType = "Read error";
                    //FD_CLR(it->sd, &ReadFDs); -- why was it here ???
                }
                // TODO: remove - writing is done separately
/*              if (FD_ISSET(it->sd, &WriteFDs)) {
                    logger->log("DEBUG: Socket became writable; handling it: ", (int)it->sd);
                    bOK = WriteData(*it);
                    pcErrorType = "Write error";
                    FD_CLR(it->sd, &WriteFDs);
                }*/
            }

            if (!bOK) {
                // Something bad happened on the socket, or the
                // client closed its half of the connection.  Shut
                // the conn down and remove it from the list.
                int err;
                int errlen = sizeof(err);
                getsockopt(it->sd, SOL_SOCKET, SO_ERROR, (char*)&err, &errlen);
                if (err != NO_ERROR) {
                    SaveLastWinsockError(pcErrorType, err);
                }
                CloseSocket(it->sd);
                it = gConnections.erase(it);
//              it = gConnections.begin();
            }
            else {
                ++it; // Go on to next connection
            }
        }//while
//  }//while
    return newclients;
}

