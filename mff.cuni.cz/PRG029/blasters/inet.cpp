#include "net.h"

#include <string>
#include <algorithm>
#include <windows.h>

#include "globals.h"
#include "logger.h"

using namespace std;

///////////////`/////////////////////////////////////////////////////////
// Constants 
#define BUFFERSIZE 4096

Connection clientConnection; // client connection to server

SOCKET gameserversock = INVALID_SOCKET;
SOCKET &gameclientsock = clientConnection.sd; //INVALID_SOCKET;

static string lastError;
static string lastErrorCode;
static string lastErrorReason;

////////////////////////////////////////////////////////
///////// INITIALIZATION
/////////
bool InitWinSock() 
{
   	WSAData wsaData;	// Start Winsock up
	int nCode;
    if ((nCode = WSAStartup(MAKEWORD(1, 1), &wsaData)) != 0) {
		SaveLastWinsockError("WSAStartup");
        return false;
    }//if
	return true;
}

//// ReadData //////////////////////////////////////////////////////////
// Data came in on a client socket, so read it into the buffer.  Returns
// false on error, or when the client closes its half of the
// connection.  (WSAEWOULDBLOCK doesn't count as a .)

bool Connection::ReadData() 
{
    char inBuffer[BUFFERSIZE+1]; // incoming data
    int nBytes = recv(sd, inBuffer, BUFFERSIZE, 0);
    if (nBytes == 0) {
        logger->log("Socket was closed by the client. ", (int)sd);
        return false;
    }//if
    else if (nBytes == SOCKET_ERROR) {
//        int errlen = sizeof(err);
//        getsockopt(sd, SOL_SOCKET, SO_ERROR, (char*)&err, &errlen);
        return (SaveLastWinsockError("recv") == WSAEWOULDBLOCK);
    }//else
    inBuffer[nBytes] = '\0';
    logger->logf("recv %i bytes", nBytes);
    acBuffer.append(inBuffer);
    return true;
}

//// WriteData /////////////////////////////////////////////////////////
// The connection is writable, so send any pending data.  Returns
// false on .  (WSAEWOULDBLOCK doesn't count as a failure.)

bool Connection::WriteData(const char* buffer) 
{
    int tries = 4;
    int start = 0;
    while ((--tries) >= 0)  {
        int l = (int)strlen(&buffer[start]);
        if (l == 0) { return true; }
        int nBytes = send(sd, &buffer[start], l, 0);
        if (nBytes == SOCKET_ERROR) {
            int err;  // Something bad happened on the socket.  Deal with it.
            int errlen = sizeof(err);
            getsockopt(sd, SOL_SOCKET, SO_ERROR, (char*)&err, &errlen);
            if (err == WSAEWOULDBLOCK) {
                return true;
            } else {
                SaveLastWinsockError("send");
                return false;
            }//if/else
        }//if
        else if (nBytes == l) {
            return true;
        }//else/if
        else {
            // We sent part of the buffer's data.
            logger->log("DEBUG: failed to send whole packet");
            start += nBytes;
        }//else
    }//while
    return true;
}

void Connection::Close()
{
    CloseSocket(sd);
    sd = INVALID_SOCKET;
}


void CleanupWinSock() 
{
    // Shut Winsock back down and take off.
    WSACleanup();
}

void CloseGameConnections()
{
    for (Connections::iterator con = gConnections.begin(); con != gConnections.end(); ++con) {
        con->WriteData(COMMAND_REJECT " Server_shutdown. \r\n");
        con->Close();
    }//for
    CloseSocket(gameserversock);
    CloseSocket(gameclientsock);
    gameserversock = INVALID_SOCKET;
    gameclientsock = INVALID_SOCKET;
}



bool CloseSocket(SOCKET sd)
{
    extern DWORD WINAPI ShutdownConnectionThread(LPVOID);

    if (sd == INVALID_SOCKET) { return false; }
    DWORD ThreadId = 0;
    return (CreateThread(NULL, 0, ShutdownConnectionThread, (LPVOID)sd, 0, &ThreadId) != NULL);
}

DWORD WINAPI ShutdownConnectionThread(LPVOID _sd)
{
    SOCKET sd = (SOCKET)_sd; // SOCKET is just some small number, sot this should be ok
    if (sd == INVALID_SOCKET) {
        return 0;
    }//if
    // Disallow any further data sends.  This will tell the other side
    // that we want to go away now.  If we skip this step, we don't
    // shut the connection down nicely.
    if (shutdown(sd, SD_SEND) == SOCKET_ERROR) {
        //return false;
    }
    // Receive any extra data still sitting on the socket.  After all
    // data is received, this call will block until the remote host
    // acknowledges the TCP control packet sent by the shutdown above.
    // Then we'll get a 0 back from recv, signalling that the remote
    // host has closed its side of the connection.
    Sleep(200); 

    const int kBufferSize = 1024;
    char acReadBuffer[1024];
    while (true) {
        int nNewBytes = recv(sd, acReadBuffer, kBufferSize, 0);
        if (nNewBytes == SOCKET_ERROR) {
            break;
        }
        else if (nNewBytes != 0) {
            //logger->log("received unexpected bytes during shutdown: ", nNewBytes);
        }
        else {
            break;// Okay, we're done!
        }
    }//while
    // Close the socket.
    closesocket(sd);
    return true;
}


const char* LastWinSockError()
{
	return lastError.c_str();
}

const char* LastWinSockErrorMessage()
{
	return (lastErrorReason+": "+lastError+" ("+lastErrorCode+")").c_str();
}

// List of Winsock error constants mapped to an interpretation string.
// Note that this list must remain sorted by the error constants'
// values, because we do a binary search on the list when looking up
// items.
static struct ErrorEntry 
{
    ErrorEntry(int id, const char* pc = NULL) : nID(id), pcMessage(pc) { }

    int nID;
    const char* pcMessage;


    bool operator<(const ErrorEntry& rhs) 
    {
        return nID < rhs.nID;
    }
} 

gaErrorList[] = {
    ErrorEntry(0,                  "No error"),
    ErrorEntry(WSAEINTR,           "Interrupted system call"),
    ErrorEntry(WSAEBADF,           "Bad file number"),
    ErrorEntry(WSAEACCES,          "Permission denied"),
    ErrorEntry(WSAEFAULT,          "Bad address"),
    ErrorEntry(WSAEINVAL,          "Invalid argument"),
    ErrorEntry(WSAEMFILE,          "Too many open sockets"),
    ErrorEntry(WSAEWOULDBLOCK,     "Operation would block"),
    ErrorEntry(WSAEINPROGRESS,     "Operation now in progress"),
    ErrorEntry(WSAEALREADY,        "Operation already in progress"),
    ErrorEntry(WSAENOTSOCK,        "Socket operation on non-socket"),
    ErrorEntry(WSAEDESTADDRREQ,    "Destination address required"),
    ErrorEntry(WSAEMSGSIZE,        "Message too long"),
    ErrorEntry(WSAEPROTOTYPE,      "Protocol wrong type for socket"),
    ErrorEntry(WSAENOPROTOOPT,     "Bad protocol option"),
    ErrorEntry(WSAEPROTONOSUPPORT, "Protocol not supported"),
    ErrorEntry(WSAESOCKTNOSUPPORT, "Socket type not supported"),
    ErrorEntry(WSAEOPNOTSUPP,      "Operation not supported on socket"),
    ErrorEntry(WSAEPFNOSUPPORT,    "Protocol family not supported"),
    ErrorEntry(WSAEAFNOSUPPORT,    "Address family not supported"),
    ErrorEntry(WSAEADDRINUSE,      "Address already in use"),
    ErrorEntry(WSAEADDRNOTAVAIL,   "Can't assign requested address"),
    ErrorEntry(WSAENETDOWN,        "Network is down"),
    ErrorEntry(WSAENETUNREACH,     "Network is unreachable"),
    ErrorEntry(WSAENETRESET,       "Net connection reset"),
    ErrorEntry(WSAECONNABORTED,    "Software caused connection abort"),
    ErrorEntry(WSAECONNRESET,      "Connection reset by peer"),
    ErrorEntry(WSAENOBUFS,         "No buffer space available"),
    ErrorEntry(WSAEISCONN,         "Socket is already connected"),
    ErrorEntry(WSAENOTCONN,        "Socket is not connected"),
    ErrorEntry(WSAESHUTDOWN,       "Can't send after socket shutdown"),
    ErrorEntry(WSAETOOMANYREFS,    "Too many references, can't splice"),
    ErrorEntry(WSAETIMEDOUT,       "Connection timed out"),
    ErrorEntry(WSAECONNREFUSED,    "Connection refused"),
    ErrorEntry(WSAELOOP,           "Too many levels of symbolic links"),
    ErrorEntry(WSAENAMETOOLONG,    "File name too long"),
    ErrorEntry(WSAEHOSTDOWN,       "Host is down"),
    ErrorEntry(WSAEHOSTUNREACH,    "No route to host"),
    ErrorEntry(WSAENOTEMPTY,       "Directory not empty"),
    ErrorEntry(WSAEPROCLIM,        "Too many processes"),
    ErrorEntry(WSAEUSERS,          "Too many users"),
    ErrorEntry(WSAEDQUOT,          "Disc quota exceeded"),
    ErrorEntry(WSAESTALE,          "Stale NFS file handle"),
    ErrorEntry(WSAEREMOTE,         "Too many levels of remote in path"),
    ErrorEntry(WSASYSNOTREADY,     "Network system is unavailable"),
    ErrorEntry(WSAVERNOTSUPPORTED, "Winsock version out of range"),
    ErrorEntry(WSANOTINITIALISED,  "WSAStartup not yet called"),
    ErrorEntry(WSAEDISCON,         "Graceful shutdown in progress"),
    ErrorEntry(WSAHOST_NOT_FOUND,  "Host not found"),
    ErrorEntry(WSANO_DATA,         "No host data of that type was found")
};
const int kNumMessages = sizeof(gaErrorList) / sizeof(ErrorEntry);

//// WSAGetLastErrorMessage ////////////////////////////////////////////
// A function similar in spirit to Unix's perror() that tacks a canned 
// interpretation of the value of WSAGetLastError() onto the end of a
// passed string, separated by a ": ".  Generally, you should implement
// smarter error handling than this, but for default cases and simple
// programs, this function is sufficient.
//

int SaveLastWinsockError(const char* reason, int nErrorID)
{
	lastError = "";
    lastErrorCode = "";
	lastErrorReason = reason;
//	lastError.append(pcMessagePrefix).append(": ");
    // Tack appropriate canned message onto end of supplied message 
    // prefix. Note that we do a binary search here: gaErrorList must be
	// sorted by the error constant's value.
	ErrorEntry* pEnd = gaErrorList + kNumMessages;
    nErrorID = nErrorID ? nErrorID : WSAGetLastError();
    ErrorEntry Target(nErrorID);
    ErrorEntry* it = lower_bound(gaErrorList, pEnd, Target);
    if ((it != pEnd) && (it->nID == Target.nID)) {
		lastError.append(it->pcMessage);
    }
    else {// Didn't find error in list, so make up a generic one
		lastError.append("unknown error");
    }
	char strID[14];
	lastErrorCode = itoa(Target.nID, strID, 10);

    if (nErrorID != WSAEWOULDBLOCK) {// log only errors
        logger->log(lastErrorReason + ": " + lastError + " (" + lastErrorCode + ")");
    }//if

    return nErrorID;
}

