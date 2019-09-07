#include <unistd.h>

#include <map>
#include <string>
#include <vector>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#include "server.h"
#include "http.h"
#include "db.h"
#include "benc.h"
#include "str.h"
#include "ctrack.h"

#define URL_ANNOUNCE "/announce?"    
#define URL_SCRAPE  "/scrape?"

// params passed in GET url
#define PARAM_INFO_HASH "info_hash" // 20byte SHA1 hash
#define PARAM_PEER_ID   "peer_id"   // 20byte peer_id
#define PARAM_PORT      "port"      // port number
#define PARAM_IP        "ip"        // client's ip
#define PARAM_UPLOADED  "uploaded"  // total number of bytes uploaded
#define PARAM_DOWNLOADED "downloaded" // total number of bytes downloaded
#define PARAM_LEFT      "left"      // bytes to left to download
#define PARAM_COMPACT   "compact"   // client accepts compact peer list
#define PARAM_NUMWANT   "numwant"   // (O) number of peers that the client want to receive
#define PARAM_KEY       "key"       // (O) clients private key
#define PARAM_TRACKERID "trackerid" // (O) id of this tracker
#define PARAM_EVENT     "event"

#define EVENT_STARTED   "started"   // client started downloading
#define EVENT_STOPPED   "stopped"   // clients shuts down
#define EVENT_COMPLETED "completed" // peer finished downloading of file

#define E_CODE_STARTED (2)
#define E_CODE_STOPPED (3)
#define E_CODE_COMPLETED (1)
#define E_CODE_NONE (0)


using namespace std;

static int get_method(const char *url);
static char *ReceiveRequest(struct ClientConnData *ccdata);
static int DecodeGet(char *buffer, HTTP_REQUEST *req);
static int SendBenc(int s, BENCDATA data);
static BENCDATA BencError(const char *error, int code);
static int GetAnnounceNodes(Peers *peers, PPeerInfo client, BENCDATA *data, int numwant);

int HTTPMain(struct ClientConnData *ccdata)
{
	HTTP_REQUEST req;
    PTorrentInfo ti;
    PPeerInfo peer;
	BENCDATA result = benc_dict_create();
	BENCDATA benc_peers;
	#define FINISH(res) shutdown(ccdata->sd, SHUT_WR);close(ccdata->sd);return(res)

    // read input
	char *input = ReceiveRequest(ccdata);
	shutdown(ccdata->sd, SHUT_RD);

	// SETUP req
    memset(&req, 0, sizeof(HTTP_REQUEST));
	req.address = ccdata->address;
    req.numwant = 50;
	if (!DecodeGet(input, &req)) { 
    	SendBenc(ccdata->sd, BencError("Invalid request", 100));
        FINISH(FALSE); 
    }
	
	DBLock();

    if (req.method == METHOD_ANNOUNCE) {
	    if (TorrentDBGet(req.info_hash, &ti, TRUE) == FALSE) {
	        DBUnlock();
	    	SendBenc(ccdata->sd, BencError("Unknown torrent", 200));
	    	FINISH(FALSE);// return error
		}

        if (FindPeer(ti, req.peer_id, &peer) == FALSE) { 
    	   UpdatePeerData(ti); // new peer
        }
        peer->ip = req.address;
        peer->port = req.port;
        peer->bytesleft = req.left;
        if (req.event == E_CODE_COMPLETED) { 
        	ti->downloaded++; // new completed download
        	UpdatePeerData(ti);
        }//if
    	logf("peers sent: %i / %i, wanted: %i",
            GetAnnounceNodes(ti->peers, peer, &benc_peers, req.numwant), 
            (int)ti->peers->size(),
            req.numwant
        );
    	benc_dict_str_add(result, "interval", benc_create_int(*announce_int));
    	benc_dict_str_add(result, "complete", benc_create_int(ti->seed_count));
    	benc_dict_str_add(result, "incomplete", benc_create_int(ti->leech_count));
    	benc_dict_str_add(result, "peers", benc_peers);
	}//if ANNOUNCE
    else { // SCRAPE
        if (TorrentDBGet(req.info_hash, &ti, FALSE) == FALSE) {
            DBUnlock();
        	SendBenc(ccdata->sd, BencError("Full scrape not supported", 101));
        	FINISH(FALSE);// return error
    	}
        BENCDATA f = benc_dict_create();
    	benc_dict_str_add(f, "downloaded", benc_create_int(ti->downloaded));
    	benc_dict_str_add(f, "complete", benc_create_int(ti->seed_count));
    	benc_dict_str_add(f, "incomplete", benc_create_int(ti->leech_count));
        benc_dict_close(f);
        BENCDATA ih = benc_dict_create();
        benc_dict_hash_add(ih, req.info_hash, f);
        benc_dict_close(ih);
        benc_dict_str_add(result, "files", ih);
    }//if SCRAPE
	DBUnlock();

    SendBenc(ccdata->sd, benc_dict_close(result));

	FINISH(TRUE); 
}

static int GetAnnounceNodes(Peers *peers, PPeerInfo client, BENCDATA *data, int numwant)
{
	BENCDATA result = benc_list_create();
    int count = 0;
    Peers::iterator it = peers->begin();
    int RCOEF = RAND_MAX;
    if (numwant < (int)peers->size()) RCOEF = (int)(RAND_MAX*numwant/peers->size());
    while (it != peers->end()) {
        PPeerInfo peer = *it;
        if ((peer != client) && (rand() < RCOEF)) {
			BENCDATA pdict = benc_dict_create();
        	benc_dict_str_add(pdict, "peer id", benc_create_hash(peer->peer_id));
        	benc_dict_str_add(pdict, "port", benc_create_int(peer->port));
	       	benc_dict_str_add(pdict, "ip", benc_create_string(inet_ntoa(peer->ip.inaddr)));
	       	benc_dict_close(pdict);
        	benc_list_add(result, pdict);
            count++;
            if (count >= numwant) break;
        }//if
        ++it;
    }//while
    *data = benc_list_close(result);
    return count;
}

static BENCDATA BencError(const char *error, int code)
{
	BENCDATA bdata = benc_dict_create();
	benc_dict_str_add(bdata, "failure reason", benc_create_string(error));
	if (code > 0) {
	   benc_dict_str_add(bdata, "failure code", benc_create_int(code));
	}
    return benc_dict_close(bdata);
}

static int SendBenc(int s, BENCDATA data)
{
	const char HEAD[] = 
		"HTTP/1.1 200 Ok\r\n" 
		"Content-Type: text/plain\r\n" 
		"Server: ctrack " VERSION "\r\n"
		"Content-Length: ";
	const char HEADEND[] = "\r\n\r\n";
	char slen[20];
	itoa(data->length, slen);
    send(s, HEAD, strlen(HEAD), 0);
    send(s, slen, strlen(slen), 0);
    send(s, HEADEND, strlen(HEADEND), 0);
    send(s, data->buffer, data->length, 0);
    benc_free(data);
    return TRUE;
}

static char *ReceiveRequest(struct ClientConnData *ccdata)
{
	char buffer[2048];
	int pos = 0;
	ssize_t in_size;
	buffer[pos] = '\0';
	while (strstr(buffer, "\r\n") == NULL) {
		if (pos > 2040) break;
		in_size = recv(ccdata->sd, &buffer[pos], 2046 - pos, 0);
		pos += (int)in_size;
 		buffer[pos] = '\0';
		if (in_size == 0) break;
	}//while
	char *endpos = strstr(buffer, "\r\n");
	if (endpos == NULL) {
	   return strdup("");
	} else {
        *endpos = '\0';
        return strdup(buffer);
    }
}

static int get_method(const char *url)
{
	if (strncmp(url, URL_ANNOUNCE, strlen(URL_ANNOUNCE)) == 0) {
		return METHOD_ANNOUNCE;
    }//if
	else if (strncmp(url, URL_SCRAPE, strlen(URL_SCRAPE)) == 0) {
		return METHOD_SCRAPE;
    }//if
	return METHOD_INVALID;
}

static int DecodeGet(char *buffer, HTTP_REQUEST *req)
{
	logf("http: %s", buffer); 
    char *method = gettoken(&buffer, " ");
    char *url = gettoken(&buffer, " ");
    char *proto = gettoken(&buffer, "\r\n");

    char *urlparams = strchr(url, '?');
    int ok = TRUE;
    if (urlparams != NULL) { urlparams += 1; }
	req->method = get_method(url);

    if (strcmp(method, "GET") != 0) {
		errorf(E_CONTINUE, "Unsupported HTTP method: %s", method);
    	ok = FALSE;  
    }//if
    else if ((strcmp(proto, "HTTP/1.0")!=0) && (strcmp(proto,"HTTP/1.1")!=0)) {
		errorf(E_CONTINUE, "Unsupported HTTP protocol: %s", proto);
    	ok = FALSE; 
    }//if
	else if (req->method == METHOD_INVALID) {
		errorf(E_CONTINUE, "Unsupported URL");
		ok = FALSE;
    }//if
	else if ((urlparams == NULL) || (urlparams[0]=='\0')) {
		errorf(E_CONTINUE, "Missing parameters in HTTP request");
		ok = FALSE;
    }//if
	else while (urlparams[0] != '\0') {
    	char *param = gettoken(&urlparams, "&;");
    	char *pval;
        int plen;
		if ((pval=strchr(param, '=')) != NULL) {
			pval[0] = '\0';
			pval = &pval[1];
			if ((plen = urldecode(pval)) <= 0) {
				errorm("invalid value for %s", param);
				ok = false;
				break;
			}
			if (strcasecmp(param, PARAM_INFO_HASH) == 0) {  memcpy(req->info_hash, pval, 20); }
			else if (strcasecmp(param, PARAM_PEER_ID) == 0) { memcpy(req->peer_id, pval, 20); }
			else if (strcasecmp(param, PARAM_PORT) == 0) { req->port = (UINT16)atoi(pval); }
			else if (strcasecmp(param, PARAM_LEFT) == 0) { req->left = (INT64)atol(pval); }
			else if (strcasecmp(param, PARAM_KEY) == 0) { req->key = strdup(pval); }
            else if (strcasecmp(param, PARAM_NUMWANT) == 0) { req->numwant = atoi(pval); }
			else if (strcasecmp(param, PARAM_EVENT) == 0) { 
				if (strcasecmp(pval, EVENT_STARTED) == 0) { req->event = E_CODE_STARTED; }
			    else if (strcasecmp(pval, EVENT_COMPLETED) == 0) { req->event = E_CODE_COMPLETED; }
			    else if (strcasecmp(pval, EVENT_STOPPED) == 0) { req->event = E_CODE_STOPPED; }
			    else { req->event = E_CODE_NONE; }
			}
			else if (strcasecmp(param, PARAM_IP) == 0) {
                if (!atoaddr(pval, &(req->address))) {
			    	req->address.addr = 0;
			    }
			}
		}//if
		else {
			errorf(E_CONTINUE, "Missing data for parameter: %s", param);
		}
		free(param);
		//param=gettoken(&urlparams, "&;");
	}//while
    //TODO: improve logging
    char p[41];
    char t[41];
    hashtostr(req->info_hash, p);
    hashtostr(req->peer_id, t);
    logf("http: torrent: %s; peer: %s, addr: %x:%i", p, t, (int)req->address.addr, req->port);

	free(method);free(proto);free(url);
    return ok;
}

